from ftplib import FTP
import uuid


class FtpService:

    def __init__(self):

        self.host = "127.0.0.1"
        self.user = "ftpuser"
        self.password = "ftppass"

    def connect(self):

        ftp = FTP(self.host)
        ftp.login(self.user, self.password)

        return ftp

    def ensure_dir(self, ftp, path):

        directories = path.split("/")

        for directory in directories:

            if directory == "":
                continue

            try:
                ftp.cwd(directory)
            except:
                ftp.mkd(directory)
                ftp.cwd(directory)

    def upload_file(self, file_stream, filename, company_id):

        ftp = self.connect()

        unique_name = f"{uuid.uuid4()}_{filename}"

        path = f"company_{company_id}"

        self.ensure_dir(ftp, path)

        ftp.storbinary(
            f"STOR {unique_name}",
            file_stream
        )

        ftp.quit()

        return f"{path}/{unique_name}"

    def delete_file(self, path):

        ftp = self.connect()

        ftp.delete(path)

        ftp.quit()