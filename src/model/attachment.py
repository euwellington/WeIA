from fastapi import UploadFile, File

class Attachment:
    def __init__(self, attachment: UploadFile = File(...)):
        self.attachment = attachment