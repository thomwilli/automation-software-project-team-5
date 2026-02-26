from sftp_upload import load_sftp_credentials, sftp_connect

if __name__ == "__main__":
    creds = load_sftp_credentials()
    sftp = None
    try:
        sftp = sftp_connect(creds)
        sftp.chdir(creds.remote_dir)
        print("✅ Connected to SFTP and changed directory successfully.")
        print("Remote directory listing:")
        for f in sftp.listdir("."):
            print(" -", f)
    finally:
        if sftp is not None:
            sftp.close()