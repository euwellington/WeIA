import os
from datetime import datetime

from src.core.celery_app import celery_app
from src.services.ftp_service import FtpService
from src.repositories.file_repository import FileRepository


@celery_app.task
def upload_file_task(
    file_id,
    company_id,
    user_id,
    folder_id,
    filename,
    temp_path,
    mime_type,
    file_size
):

    ftp_service = FtpService()
    file_repository = FileRepository()

    try:

        file_repository.update_status(
            file_id,
            "UPLOADING",
            datetime.now()
        )

        with open(temp_path, "rb") as f:
            ftp_path = ftp_service.upload_file(
                f,
                filename,
                company_id
            )

        file_repository.finish_upload(
            file_id,
            ftp_path,
            datetime.now()
        )

        return {
            "status": "UPLOADED",
            "file_id": file_id
        }

    except Exception:

        file_repository.update_status(
            file_id,
            "ERROR",
            datetime.now()
        )

        raise

    finally:

        if os.path.exists(temp_path):
            os.remove(temp_path)