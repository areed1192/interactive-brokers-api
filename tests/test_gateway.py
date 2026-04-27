"""Tests for the ClientPortalGateway utility."""


import io
import zipfile
from unittest.mock import MagicMock, patch

import pytest
import requests

from ibc.exceptions import IBCError
from ibc.utils.gateway import DEFAULT_GATEWAY_URL, DOWNLOAD_TIMEOUT, ClientPortalGateway

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def gateway(tmp_path):
    """Create a ClientPortalGateway pointing at a temp directory."""
    gw = ClientPortalGateway()
    gw._resources_folder = tmp_path / "resources"
    gw._gateway_folder = gw._resources_folder / "clientportal.beta.gw"
    return gw


@pytest.fixture
def installed_gateway(gateway):
    """Create a gateway with the marker file already present."""
    marker = gateway._gateway_folder / "bin"
    marker.mkdir(parents=True)
    (marker / "run.bat").touch()
    (marker / "run.sh").touch()
    return gateway


def _make_zip_bytes(*names: str) -> bytes:
    """Build an in-memory zip with the given entry names."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        for name in names:
            zf.writestr(name, "content")
    return buf.getvalue()


# ---------------------------------------------------------------------------
# __repr__ tests
# ---------------------------------------------------------------------------


class TestRepr:
    """Tests for ClientPortalGateway repr."""

    def test_repr_contains_resources_path(self, gateway):
        """Verify __repr__ includes the resources folder path."""
        result = repr(gateway)
        assert "ClientPortalGateway(resources=" in result
        assert "resources" in result


# ---------------------------------------------------------------------------
# _is_gateway_installed tests
# ---------------------------------------------------------------------------


class TestIsGatewayInstalled:
    """Tests for the _is_gateway_installed check."""

    def test_returns_false_when_folder_missing(self, gateway):
        """Verify returns False when gateway folder does not exist."""
        assert gateway._is_gateway_installed() is False

    def test_returns_false_when_marker_missing(self, gateway):
        """Verify returns False when folder exists but marker file is absent."""
        gateway._gateway_folder.mkdir(parents=True)
        assert gateway._is_gateway_installed() is False

    def test_returns_true_when_marker_present(self, installed_gateway):
        """Verify returns True when the expected marker file exists."""
        assert installed_gateway._is_gateway_installed() is True


# ---------------------------------------------------------------------------
# _make_resources_directory tests
# ---------------------------------------------------------------------------


class TestMakeResourcesDirectory:
    """Tests for resource directory creation."""

    def test_creates_directory_when_missing(self, gateway):
        """Verify directory is created when it doesn't exist."""
        gateway._make_resources_directory()
        assert gateway._resources_folder.exists()

    def test_noop_when_directory_exists(self, gateway):
        """Verify no error when directory already exists."""
        gateway._resources_folder.mkdir(parents=True)
        gateway._make_resources_directory()
        assert gateway._resources_folder.exists()


# ---------------------------------------------------------------------------
# _download_client_portal tests
# ---------------------------------------------------------------------------


class TestDownloadClientPortal:
    """Tests for the gateway download method."""

    @patch("ibc.utils.gateway.requests.get")
    def test_successful_download(self, mock_get, gateway):
        """Verify successful download returns the response."""
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        result = gateway._download_client_portal()

        mock_get.assert_called_once_with(url=DEFAULT_GATEWAY_URL, timeout=DOWNLOAD_TIMEOUT)
        assert result is mock_response

    @patch("ibc.utils.gateway.requests.get")
    def test_uses_custom_url(self, mock_get):
        """Verify custom download URL is used when provided."""
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        gw = ClientPortalGateway(download_url="https://example.com/gw.zip")
        gw._download_client_portal()

        mock_get.assert_called_once_with(url="https://example.com/gw.zip", timeout=DOWNLOAD_TIMEOUT)

    @patch("ibc.utils.gateway.requests.get")
    def test_raises_ibc_error_on_http_error(self, mock_get, gateway):
        """Verify IBCError is raised when HTTP request fails."""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("404")
        mock_get.return_value = mock_response

        with pytest.raises(IBCError, match="Failed to download"):
            gateway._download_client_portal()

    @patch("ibc.utils.gateway.requests.get")
    def test_raises_ibc_error_on_connection_error(self, mock_get, gateway):
        """Verify IBCError is raised on network failure."""
        mock_get.side_effect = requests.ConnectionError("no route")

        with pytest.raises(IBCError, match="Failed to download"):
            gateway._download_client_portal()


# ---------------------------------------------------------------------------
# _create_zip_file tests
# ---------------------------------------------------------------------------


class TestCreateZipFile:
    """Tests for zip file creation from response content."""

    def test_creates_valid_zip(self, gateway):
        """Verify a valid zip response produces a ZipFile object."""
        mock_response = MagicMock()
        mock_response.content = _make_zip_bytes("test.txt")

        result = gateway._create_zip_file(mock_response)

        assert isinstance(result, zipfile.ZipFile)
        assert "test.txt" in result.namelist()

    def test_raises_ibc_error_on_invalid_content(self, gateway):
        """Verify IBCError is raised when content is not a valid zip."""
        mock_response = MagicMock()
        mock_response.content = b"this is not a zip file"

        with pytest.raises(IBCError, match="not a valid zip file"):
            gateway._create_zip_file(mock_response)


# ---------------------------------------------------------------------------
# _validate_zip_entries tests
# ---------------------------------------------------------------------------


class TestValidateZipEntries:
    """Tests for zip path traversal validation."""

    def test_safe_entries_pass(self, gateway):
        """Verify validation passes for normal entries."""
        buf = io.BytesIO(_make_zip_bytes("bin/run.bat", "lib/config.yaml"))
        zf = zipfile.ZipFile(buf)

        gateway._validate_zip_entries(zf)

    def test_dotdot_path_raises(self, gateway):
        """Verify path traversal via .. is rejected."""
        buf = io.BytesIO(_make_zip_bytes("../../etc/passwd"))
        zf = zipfile.ZipFile(buf)

        with pytest.raises(IBCError, match="Unsafe path"):
            gateway._validate_zip_entries(zf)

    def test_absolute_path_raises(self, gateway):
        """Verify absolute paths starting with / are rejected."""
        buf = io.BytesIO(_make_zip_bytes("/etc/passwd"))
        zf = zipfile.ZipFile(buf)

        with pytest.raises(IBCError, match="Unsafe path"):
            gateway._validate_zip_entries(zf)


# ---------------------------------------------------------------------------
# _extract_zip_file tests
# ---------------------------------------------------------------------------


class TestExtractZipFile:
    """Tests for zip extraction."""

    def test_extracts_to_gateway_folder(self, gateway):
        """Verify extraction goes to the gateway folder path."""
        gateway._resources_folder.mkdir(parents=True)
        buf = io.BytesIO(_make_zip_bytes("test.txt"))
        zf = zipfile.ZipFile(buf)

        gateway._extract_zip_file(zf)

        assert (gateway._gateway_folder / "test.txt").exists()

    def test_rejects_unsafe_zip(self, gateway):
        """Verify extraction is blocked for unsafe zip entries."""
        gateway._resources_folder.mkdir(parents=True)
        buf = io.BytesIO(_make_zip_bytes("../escape.txt"))
        zf = zipfile.ZipFile(buf)

        with pytest.raises(IBCError, match="Unsafe path"):
            gateway._extract_zip_file(zf)


# ---------------------------------------------------------------------------
# setup tests
# ---------------------------------------------------------------------------


class TestSetup:
    """Tests for the setup orchestration method."""

    def test_skips_download_when_already_installed(self, installed_gateway):
        """Verify setup is a no-op when gateway is already installed."""
        with patch.object(installed_gateway, "_download_client_portal") as mock_dl:
            installed_gateway.setup()
            mock_dl.assert_not_called()

    @patch("ibc.utils.gateway.requests.get")
    def test_downloads_and_extracts_when_not_installed(self, mock_get, gateway):
        """Verify full setup flow runs when gateway is missing."""
        zip_bytes = _make_zip_bytes("bin/run.bat", "bin/run.sh", "lib/config.yaml")
        mock_response = MagicMock()
        mock_response.content = zip_bytes
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        gateway.setup()

        assert gateway._gateway_folder.exists()
        assert (gateway._gateway_folder / "bin" / "run.bat").exists()

    @patch("ibc.utils.gateway.requests.get")
    def test_setup_raises_on_download_failure(self, mock_get, gateway):
        """Verify setup propagates IBCError on download failure."""
        mock_get.side_effect = requests.ConnectionError("offline")

        with pytest.raises(IBCError, match="Failed to download"):
            gateway.setup()

    @patch("ibc.utils.gateway.requests.get")
    def test_setup_raises_on_corrupt_zip(self, mock_get, gateway):
        """Verify setup propagates IBCError on corrupt download."""
        mock_response = MagicMock()
        mock_response.content = b"not a zip"
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        with pytest.raises(IBCError, match="not a valid zip file"):
            gateway.setup()
