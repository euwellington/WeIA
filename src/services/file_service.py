import hashlib
from src.services.ftp_service import FtpService
from src.repositories.file_repository import FileRepository
from src.services.attachment_service import AttachmentService
from src.model.attachment import Attachment


class FileService:

    def __init__(self):
        self.ftp_service = FtpService()
        self.file_repository = FileRepository()
        self.attachment_service = AttachmentService()


    def generate_hash(self, file):

        sha256 = hashlib.sha256()

        while True:
            chunk = file.read(8192)

            if not chunk:
                break

            sha256.update(chunk)

        file.seek(0)

        return sha256.hexdigest()

    async def upload_file(self, company_id, user_id, folder_id, file):
        
        attachment = Attachment(file)
        
        attachment.attachment = file
        
        result = await self.attachment_service.attachment_file(attachment)

        if result.get("erro"):
            raise "Erro ao salvar no vetorial"
        
        filename = file.filename

        file_hash = self.generate_hash(file.file)

        existing_file = self.file_repository.get_by_hash(file_hash)

        if existing_file:
            return {
                "id": existing_file["id"],
                "path": existing_file["ftp_path"],
                "status": "already_exists"
            }

        ftp_path = self.ftp_service.upload_file(
            file.file,
            filename,
            company_id
        )

        file_size = file.size if hasattr(file, "size") else None

        mime_type = file.content_type

        file_id = self.file_repository.create(
            company_id,
            user_id,
            folder_id,
            filename,
            filename,
            file_size,
            mime_type,
            ftp_path,
            file_hash
        )

        return {
            "id": file_id,
            "path": ftp_path,
            "status": "uploaded"
        }

    def delete_file(self, file_id):

        file = self.file_repository.get_by_id(file_id)

        if not file:
            return None

        self.ftp_service.delete_file(file["ftp_path"])

        self.file_repository.delete(file_id)

        return True

    def list_files(self, folder_id):

        return self.file_repository.list_by_folder(folder_id)