from __future__ import annotations

import io
import logging
import pathlib
import sys
import zipfile

import requests

from ibc.exceptions import IBCError

logger = logging.getLogger(__name__)

DEFAULT_GATEWAY_URL = "https://download2.interactivebrokers.com/portal/clientportal.beta.gw.zip"
DOWNLOAD_TIMEOUT = 60
EXPECTED_MARKER = "bin/run.bat" if sys.platform == "win32" else "bin/run.sh"


class ClientPortalGateway():

    def __init__(self, download_url: str = DEFAULT_GATEWAY_URL) -> None:
        """Initializes the client portal object.

        ### Parameters
        ----
        download_url : str (optional)
            The URL to download the Client Portal Gateway zip from.
            Defaults to the official Interactive Brokers download URL.
        """

        self._download_url = download_url
        self._resources_folder = (
            pathlib.Path(__file__).parent.parent / "resources"
        ).resolve()
        self._gateway_folder = self._resources_folder / "clientportal.beta.gw"

    def __repr__(self) -> str:
        return f"ClientPortalGateway(resources={self._resources_folder})"

    def _is_gateway_installed(self) -> bool:
        """Checks if the gateway is already installed with expected files.

        ### Returns
        ----
        bool:
            `True` if the gateway folder exists and contains the expected marker file.
        """

        return (self._gateway_folder / EXPECTED_MARKER).exists()

    def _make_resources_directory(self) -> None:
        """Makes the resource folder if it doesn't exist."""

        if not self._resources_folder.exists():
            logger.info("Gateway folder does not exist, creating...")
            self._resources_folder.mkdir(parents=True)

    def _download_client_portal(self) -> requests.Response:
        """Downloads the Client Portal from Interactive Brokers.

        ### Returns
        ----
        requests.Response:
            A response object with clientportal content.

        ### Raises
        ----
        IBCError:
            If the download fails or returns a non-200 status.
        """

        try:
            response = requests.get(url=self._download_url, timeout=DOWNLOAD_TIMEOUT)
            response.raise_for_status()
        except requests.RequestException as exc:
            raise IBCError(f"Failed to download Client Portal Gateway from {self._download_url}") from exc

        return response

    def _create_zip_file(self, response_content: requests.Response) -> zipfile.ZipFile:
        """Creates a zip file to house the client portal content.

        ### Parameters
        ----
        response_content: requests.Response
            The response object with the client portal content.

        ### Returns
        ----
        zipfile.ZipFile:
            A zip file object with the Client Portal.

        ### Raises
        ----
        IBCError:
            If the downloaded content is not a valid zip file.
        """

        try:
            zip_file_content = zipfile.ZipFile(
                io.BytesIO(response_content.content)
            )
        except zipfile.BadZipFile as exc:
            raise IBCError("Downloaded content is not a valid zip file") from exc

        return zip_file_content

    @staticmethod
    def _validate_zip_entries(zip_file: zipfile.ZipFile) -> None:
        """Validates zip entries to prevent path traversal attacks.

        ### Parameters
        ----
        zip_file: zipfile.ZipFile
            The zip file to validate.

        ### Raises
        ----
        IBCError:
            If any zip entry contains a path traversal sequence.
        """

        for entry in zip_file.namelist():
            if ".." in entry or entry.startswith("/"):
                raise IBCError(f"Unsafe path detected in zip archive: {entry!r}")

    def _extract_zip_file(self, zip_file: zipfile.ZipFile) -> None:
        """Extracts the Zip File after validating entries.

        ### Parameters
        ----
        zip_file: zipfile.ZipFile:
            The client portal zip file to be extracted.

        ### Raises
        ----
        IBCError:
            If any zip entry contains a path traversal sequence.
        """

        self._validate_zip_entries(zip_file)
        zip_file.extractall(path=self._gateway_folder)

    def setup(self) -> None:
        """Downloads and extracts the client portal object.

        Skips download if the gateway is already installed with expected files.

        ### Raises
        ----
        IBCError:
            If the download, zip parsing, or extraction fails.
        """

        if self._is_gateway_installed():
            logger.info("Gateway already installed at %s", self._gateway_folder)
            return

        self._make_resources_directory()

        # Download it.
        logger.info("Downloading Client Portal Gateway...")
        client_portal_response = self._download_client_portal()

        # Create a zip file.
        client_portal_zip = self._create_zip_file(
            response_content=client_portal_response
        )
        logger.info("Zip folder created...")

        # Extract it.
        self._extract_zip_file(zip_file=client_portal_zip)
        logger.info("Files extracted. New folder is: %s", self._gateway_folder)
