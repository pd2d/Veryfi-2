import os
from veryfi import Client


class VeryfiAPI :
    
    VERYFI_CLIENT_ID = 'vrfvR6RP1tZTjWH6dlpFpmuKhZtPK5m9lw2iHUL'
    VERYFI_CLIENT_SECRET = 'rWD7p7YCbFv2Nn9FvNVbfn3VduDtfnBSDvNnJDKMxXgm9SO39TD5p1rPPcs8HIACigxPI2RJPy0jFCrNpZi6WGJOOIwENe6tIrIouUlKh8d8LYbaWgEEAFbORmCni1wO'
    VERYFI_USERNAME = 'manu.benny'
    VERYFI_API_KEY = '656e869c937690ef2c8797b4089d54c8'

    DELETE_AFTER_PROCESSING = True

    def __init__(self):
        self.client = Client(
            self.VERYFI_CLIENT_ID,
            self.VERYFI_CLIENT_SECRET,
            self.VERYFI_USERNAME,
            self.VERYFI_API_KEY,
        )

    def process_document(
        self,
        file_path,
    ):
        """
        sends the document to veryfi and receives the process OCR data in response
        """
        response = self.client.process_document(
            file_path=file_path, delete_after_processing=self.DELETE_AFTER_PROCESSING
        )
        return response

client = VeryfiAPI()
response = client.process_document(file_path="bill_image/Adobe Scan 28-Dec-2023 (5)_page-0001.jpg")
print(response)