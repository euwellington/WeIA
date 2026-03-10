from src.workers.upload_tasks import upload_file_task


class QueueService:

    def send_upload_job(
        self,
        file_id: int,
        company_id: int,
        user_id: int,
        folder_id: int,
        filename: str,
        temp_path: str,
        mime_type: str,
        file_size: int
    ):

        task = upload_file_task.delay(
            file_id,
            company_id,
            user_id,
            folder_id,
            filename,
            temp_path,
            mime_type,
            file_size
        )

        return task.id