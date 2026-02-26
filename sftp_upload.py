import os
from dataclasses import dataclass
from typing import Optional

import paramiko
from dotenv import load_dotenv


@dataclass
class SFTPCredentials:
    host: str
    port: int
    username: str
    password: str
    remote_dir: str


def load_sftp_credentials() -> SFTPCredentials:
    load_dotenv()

    host = os.getenv("SFTP_HOST")
    port_str = os.getenv("SFTP_PORT", "22")
    username = os.getenv("SFTP_USERNAME")
    password = os.getenv("SFTP_PASSWORD")
    remote_dir = os.getenv("SFTP_REMOTE_DIR")

    missing = [k for k, v in {
        "SFTP_HOST": host,
        "SFTP_USERNAME": username,
        "SFTP_PASSWORD": password,
        "SFTP_REMOTE_DIR": remote_dir,
    }.items() if not v]

    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

    return SFTPCredentials(
        host=host,
        port=int(port_str),
        username=username,
        password=password,
        remote_dir=remote_dir,
    )


def sftp_connect(creds: SFTPCredentials) -> paramiko.SFTPClient:
    transport = paramiko.Transport((creds.host, creds.port))
    transport.connect(username=creds.username, password=creds.password)
    return paramiko.SFTPClient.from_transport(transport)


def upload_csv(local_csv_path: str, remote_filename: str, creds: Optional[SFTPCredentials] = None) -> str:
    if creds is None:
        creds = load_sftp_credentials()

    if not os.path.exists(local_csv_path):
        raise FileNotFoundError(f"Local file not found: {local_csv_path}")

    sftp = None
    try:
        sftp = sftp_connect(creds)
        sftp.chdir(creds.remote_dir)

        remote_path = f"{creds.remote_dir.rstrip('/')}/{remote_filename}"
        sftp.put(local_csv_path, remote_path)

        stat = sftp.stat(remote_path)
        if stat.st_size <= 0:
            raise RuntimeError("Upload completed but remote file size is 0 bytes.")

        print(f"✅ Uploaded {local_csv_path} → {remote_path} ({stat.st_size} bytes)")
        return remote_path

    finally:
        if sftp is not None:
            sftp.close()