import os
import cv2
from veryfi import Client
from .models import Invoice
from django.shortcuts import render
from rest_framework import status
from .models import Invoice, LineItem
from rest_framework.response import Response
# from .serializers import VeryfiAPISerializer
from rest_framework.decorators import api_view
from django.conf import settings
from django.core.files.storage import default_storage
from .serializers import ViewSerializer, inlineSerializer

class VeryfiAPI :
    """
    Wrapper for accessing the Veryfi API's
    API documentation: https://veryfi.github.io/veryfi-python/reference/veryfi/#client
    """

    VERYFI_CLIENT_ID = 'vrfvR6RP1tZTjWH6dlpFpmuKhZtPK5m9lw2iHUL'
    VERYFI_CLIENT_SECRET = 'rWD7p7YCbFv2Nn9FvNVbfn3VduDtfnBSDvNnJDKMxXgm9SO39TD5p1rPPcs8HIACigxPI2RJPy0jFCrNpZi6WGJOOIwENe6tIrIouUlKh8d8LYbaWgEEAFbORmCni1wO'
    VERYFI_USERNAME = 'manu.benny'
    VERYFI_API_KEY = '656e869c937690ef2c8797b4089d54c8'
    # Base json to store as default value in the document table
    ITEM_BASE = [
        {
            "id": None,
            "sku": None,
            "tax": None,
            "upc": None,
            "date": None,
            "tags": None,
            "text": None,
            "type": None,
            "order": None,
            "price": None,
            "total": None,
            "section": None,
            "discount": None,
            "end_date": None,
            "quantity": None,
            "tax_rate": None,
            "reference": None,
            "start_date": None,
            "description": None,
            "discount_rate": None,
            "unit_of_measure": None,
        }
    ]
    BASE_JSON = {
        "id": None,
        "tax": None,
        "tip": None,
        "date": None,
        "notes": None,
        "total": None,
        "vendor": {
            "lat": None,
            "lng": None,
            "web": None,
            "iban": None,
            "logo": None,
            "name": None,
            "type": None,
            "email": None,
            "address": None,
            "category": None,
            "raw_name": None,
            "bank_name": None,
            "abn_number": None,
            "bank_swift": None,
            "fax_number": None,
            "reg_number": None,
            "vat_number": None,
            "bank_number": None,
            "raw_address": None,
            "phone_number": None,
            "account_number": None,
        },
        "bill_to": {
            "name": None,
            "address": None,
            "vat_number": None,
            "parsed_address": None,
        },
        "img_url": None,
        "payment": {
            "type": None,
            "terms": None,
            "card_number": None,
            "display_name": None,
        },
        "pdf_url": None,
        "ship_to": {"name": None, "address": None, "parsed_address": None},
        "cashback": None,
        "category": None,
        "discount": None,
        "due_date": None,
        "ocr_text": None,
        "rounding": None,
        "shipping": None,
        "subtotal": None,
        "insurance": None,
        "ship_date": None,
        "tax_lines": [],
        "line_items": ITEM_BASE,
        "order_date": None,
        "external_id": None,
        "is_money_in": True,
        "created_date": None,
        "duplicate_of": None,
        "is_duplicate": False,
        "store_number": None,
        "total_weight": None,
        "updated_date": None,
        "currency_code": None,
        "delivery_date": None,
        "document_type": None,
        "img_file_name": None,
        "account_number": None,
        "document_title": None,
        "invoice_number": None,
        "tracking_number": None,
        "reference_number": None,
        "service_end_date": None,
        "img_thumbnail_url": None,
        "service_start_date": None,
        "purchase_order_number": None,
        "document_reference_number": None,
    }
    DELETE_AFTER_PROCESSING = True

    def __init__(self):
        self.client = Client(
            self.VERYFI_CLIENT_ID,
            self.VERYFI_CLIENT_SECRET,
            self.VERYFI_USERNAME,
            self.VERYFI_API_KEY,
        )

    def process_document(self,file_path,):
#======================================================================================
        image = cv2.imread(file_path)

        if not self.is_image_clear(image):
            return {"message": "Image is not clear"}
        
        if self.is_bill_torn(image):
            return {"message": "Bill is torn"}
#=======================================================================================       

        """
        sends the document to veryfi and receives the process OCR data in response
        """
        processed_data  = self.client.process_document(
            file_path=file_path, delete_after_processing=self.DELETE_AFTER_PROCESSING
        )

        return processed_data
#=======================================================================================   
    def is_image_clear(self, image, threshold=100):
        # Simple example: Check if the image has sufficient contrast (you can customize based on your requirements)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, contrast = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY)
        return cv2.countNonZero(contrast) > threshold

    def is_bill_torn(self, image, tear_threshold=0.9):
        # Simple example: Check if the image has a significant tear (you can customize based on your requirements)
        # This example assumes that a torn bill will have a large region with low contrast
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, contrast = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY)
        white_pixels = cv2.countNonZero(contrast)
        total_pixels = image.shape[0] * image.shape[1]
        tear_ratio = 1 - (white_pixels / total_pixels)
        return tear_ratio > tear_threshold
    
#======================================================================================

@api_view(['POST'])
def my_view(request):
    if request.method == 'POST':
        file = request.FILES.get('images')
        if file:
            # Create the directory if it doesn't exist
            media_root = settings.MEDIA_ROOT
            if not os.path.exists(media_root):
                os.makedirs(media_root)

            # Save the uploaded file to a temporary location
            temp_file_path = os.path.join(media_root, file.name)
            with default_storage.open(temp_file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            # Process the document
            client = VeryfiAPI()
            processed_data = client.process_document(file_path=temp_file_path)

            # Clean up: delete the temporary file
            # os.remove(temp_file_path)

            # Extract relevant data from the processed Veryfi data
            invoice_data = {
                "account_number": processed_data.get('account_number'),
                "bill_to_name": processed_data.get('bill_to', {}).get('name'),
                "bill_to_address": processed_data.get('bill_to', {}).get('address'),
                #"date": processed_data.get('date'),
                
                
                # ... (add other fields as needed)
            }
            account_num = invoice_data.get("account_number")
            
            if account_num is None:
                return Response({'message': 'The bill is not valid. bill number is missing.'}, status=status.HTTP_400_BAD_REQUEST)

            existing_invoice = Invoice.objects.filter(
                account_number=invoice_data["account_number"],
                bill_to_name=invoice_data["bill_to_name"],
                bill_to_address=invoice_data["bill_to_address"],).first()
            
            


            if existing_invoice:
                return Response({'message': 'Invoice already exists. You have already applied.'}, status=status.HTTP_400_BAD_REQUEST)
            
            

            # Create and save the Invoice object
            invoice = Invoice(**invoice_data)
            invoice.save()


        # Extract line items data
            line_items_data = processed_data.get('line_items', [])
            for item_data in line_items_data:
                line_item = LineItem(
                    invoice=invoice,
                    date=item_data.get('date'),
                    description=item_data.get('description'),
                    # ... (add other fields as needed)
                )
                #line_item = LineItem(**line_items)
                line_item.save()

            return Response({'message': 'Data inserted successfully'}, status=status.HTTP_201_CREATED)
            #return Response(processed_data, status=status.HTTP_201_CREATED)
            
        else:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
@api_view(['GET'])
def data(request):
     data = Invoice.objects.all()
     serializer = ViewSerializer(data, many=True)
     return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def datas(request):
     data = LineItem.objects.all()
     serializer = inlineSerializer(data, many=True)
     return Response(serializer.data, status=status.HTTP_200_OK)


#=========================================================================
#for test case 
# @api_view(['DELETE'])m
# def delete(request):
#     user = request.user
#     order_items = Invoice.objects.filter(user=user)

#     order_items.delete()
#     return Response({"message": "deleted all orders"}, status=status.HTTP_204_NO_CONTENT)