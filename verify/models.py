from django.db import models

class Invoice(models.Model):
    account_number = models.CharField(max_length=255, null=True)
    bill_to_name = models.CharField(max_length=255, null=True)
    bill_to_address = models.TextField(null=True)
    # date = models.DateTimeField()
    # total = models.FloatField()
    #category = models.CharField(max_length=255)
    #created_date = models.DateTimeField()
    #currency_code = models.CharField(max_length=3)
    #document_reference_number = models.CharField(max_length=255)
    #document_type = models.CharField(max_length=255)
    #invoice_number = models.CharField(max_length=255)
    #is_duplicate = models.BooleanField()
    #is_money_in = models.BooleanField()
    #meta_owner = models.CharField(max_length=255)
    #notes = models.TextField(null=True, blank=True)
    #ocr_text = models.TextField()
    #order_date = models.DateTimeField(null=True, blank=True)
    #pdf_url = models.URLField(null=True, blank=True)
    #reference_number = models.CharField(max_length=255)
    #rounding = models.FloatField(null=True, blank=True)
    #service_end_date = models.DateTimeField(null=True, blank=True)
    #service_start_date = models.DateTimeField(null=True, blank=True)
    #ship_date = models.DateTimeField(null=True, blank=True)
    #store_number = models.CharField(max_length=255)
    #subtotal = models.FloatField()
    #tax = models.FloatField()
    #tip = models.FloatField()
    #updated_date = models.DateTimeField()
    
    # Add other fields as needed based on your requirements
    
    class Meta:
        verbose_name_plural = "Invoices"

class LineItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='line_items', on_delete=models.CASCADE)
    date = models.DateTimeField(null=True, blank=True)
    description = models.CharField(max_length=255, null=False)
    #discount = models.FloatField(null=True, blank=True)
    #discount_rate = models.FloatField(null=True, blank=True)
    # Add other fields as needed based on your requirements
    
    class Meta:
        verbose_name_plural = "Line Items"

    @classmethod
    def save_line_items(cls, invoice, line_items_data):
        for item_data in line_items_data:
            line_item = cls(
                invoice=invoice,
                date=item_data.get('date'),
                description=item_data.get('description'),
                # Add other fields as needed based on your requirements
            )
            line_item.save()
