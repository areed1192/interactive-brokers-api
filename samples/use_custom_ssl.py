"""Example usage of custom SSL certificates with the IB Client Portal Gateway."""

import subprocess
import sys
from configparser import ConfigParser
from pathlib import Path

from ibc.client import InteractiveBrokersClient

# ---------------------------------------------------------------------------
# Configuration — adjust these paths to your environment
# ---------------------------------------------------------------------------

# Where to generate the keystore and certificate files.
OUTPUT_DIR = Path("certs")
KEYSTORE_PATH = OUTPUT_DIR / "gateway.jks"
PEM_CERT_PATH = OUTPUT_DIR / "gateway-ca.pem"

# Keystore and certificate settings.
KEYSTORE_PASSWORD = "changeit"
KEY_ALIAS = "ibgateway"
VALIDITY_DAYS = 730  # 2 years
DNAME = "CN=localhost, OU=Development, O=MyOrg, L=City, ST=State, C=US"

# Path to the gateway's keystore (overwritten with our custom one).
GATEWAY_KEYSTORE = Path("ibc/resources/clientportal.beta.gw/root/vertx.jks")

# ---------------------------------------------------------------------------
# Step 1 — Generate a Java KeyStore with a self-signed certificate
# ---------------------------------------------------------------------------
# The IB Client Portal Gateway reads its TLS certificate from a JKS file.
# We use Java's `keytool` to create a new keypair and self-signed cert.

OUTPUT_DIR.mkdir(exist_ok=True)

print("Generating Java KeyStore with a self-signed certificate...")
subprocess.run(
    [
        "keytool",
        "-genkeypair",
        "-alias",
        KEY_ALIAS,
        "-keyalg",
        "RSA",
        "-keysize",
        "2048",
        "-validity",
        str(VALIDITY_DAYS),
        "-keystore",
        str(KEYSTORE_PATH),
        "-storepass",
        KEYSTORE_PASSWORD,
        "-dname",
        DNAME,
        "-ext",
        "SAN=dns:localhost,ip:127.0.0.1",
    ],
    check=True,
)
print(f"  KeyStore created: {KEYSTORE_PATH}")
# Output: KeyStore created: certs/gateway.jks

# ---------------------------------------------------------------------------
# Step 2 — Export the certificate to PEM format for Python
# ---------------------------------------------------------------------------
# Python's `requests` (and `urllib3`) expect PEM-encoded certificates.
# Export the public certificate from the JKS so we can pass it to verify_ssl.

# First export to DER format, then convert to PEM.
der_path = OUTPUT_DIR / "gateway-ca.der"

subprocess.run(
    [
        "keytool",
        "-exportcert",
        "-alias",
        KEY_ALIAS,
        "-keystore",
        str(KEYSTORE_PATH),
        "-storepass",
        KEYSTORE_PASSWORD,
        "-file",
        str(der_path),
    ],
    check=True,
)

# Convert DER → PEM using openssl (available on most systems).
subprocess.run(
    [
        "openssl",
        "x509",
        "-inform",
        "DER",
        "-in",
        str(der_path),
        "-out",
        str(PEM_CERT_PATH),
        "-outform",
        "PEM",
    ],
    check=True,
)

der_path.unlink()  # Clean up the intermediate DER file.
print(f"  PEM certificate exported: {PEM_CERT_PATH}")
# Output: PEM certificate exported: certs/gateway-ca.pem

# ---------------------------------------------------------------------------
# Step 3 — Install the keystore for the gateway
# ---------------------------------------------------------------------------
# Copy the new keystore over the gateway's default vertx.jks.
# Also update `sslPwd` in root/conf.yaml to match KEYSTORE_PASSWORD.

# NOTE: Uncomment the lines below to actually overwrite the gateway keystore.
# import shutil
# shutil.copy(KEYSTORE_PATH, GATEWAY_KEYSTORE)
# print(f"  Copied keystore to {GATEWAY_KEYSTORE}")

print("\nTo complete setup, copy the keystore manually:")
print(f"  cp {KEYSTORE_PATH} {GATEWAY_KEYSTORE}")
print(f"  Then update 'sslPwd' in root/conf.yaml to: {KEYSTORE_PASSWORD}")

# ---------------------------------------------------------------------------
# Step 4 — Use the custom certificate with the client
# ---------------------------------------------------------------------------
# Pass the PEM certificate path as `verify_ssl` to enable SSL verification
# against your custom certificate instead of disabling verification entirely.
#
# Why this works: when you pass a file path to `verify_ssl`, Python's
# `requests` library uses that PEM file as its trusted CA bundle. A
# self-signed certificate IS its own Certificate Authority, so the server
# cert matches the CA bundle and verification succeeds — no warnings,
# no errors from the Python client.
#
# NOTE: Your browser will still show a security warning when opening the
# gateway login page (https://localhost:5000) because the browser has its
# own trust store. This is expected — just click through the warning to
# authenticate. The Python client won't have this problem.

if not PEM_CERT_PATH.exists():
    print("PEM certificate not found — skipping client example.", file=sys.stderr)
    sys.exit(1)

config = ConfigParser()
config.read("config/config.ini")

account_number = config.get("interactive_brokers_paper", "paper_account")
account_password = config.get("interactive_brokers_paper", "paper_password")

ibc_client = InteractiveBrokersClient(
    account_number=account_number,
    password=account_password,
    verify_ssl=str(PEM_CERT_PATH),
)

print(f"\nClient created with verify_ssl={ibc_client.session.verify_ssl!r}")
# Output: Client created with verify_ssl='certs/gateway-ca.pem'

# Authenticate and use the client as normal.
ibc_client.authentication.wait_for_login()
print(ibc_client.session.health_check())
# Output: True
