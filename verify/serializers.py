from rest_framework import serializers
from .models import Invoice, LineItem
#from .views import VeryfiAPI

class VeryfiAPISerializer(serializers.Serializer):
    account_number = serializers.CharField()
    bill_to = serializers.DictField(child=serializers.CharField(), allow_null=True)
    cashback = serializers.FloatField(allow_null=True)
    category = serializers.CharField()
    created_date = serializers.DateTimeField()
    currency_code = serializers.CharField()
    date = serializers.DateTimeField(allow_null=True)
    delivery_date = serializers.DateTimeField(allow_null=True)
    discount = serializers.FloatField(allow_null=True)
    document_reference_number = serializers.CharField(allow_null=True)
    document_title = serializers.CharField(allow_null=True)
    document_type = serializers.CharField()
    due_date = serializers.DateTimeField(allow_null=True)
    duplicate_of = serializers.IntegerField(allow_null=True)
    external_id = serializers.CharField(allow_null=True)
    id = serializers.IntegerField()
    img_file_name = serializers.CharField()
    img_thumbnail_url = serializers.CharField(allow_null=True)
    img_url = serializers.CharField(allow_null=True)
    insurance = serializers.CharField(allow_null=True)
    invoice_number = serializers.CharField()
    is_duplicate = serializers.BooleanField()
    is_money_in = serializers.CharField(allow_null=True)
    #line_items = LineItemSerializer(many=True)
    meta = serializers.DictField(child=serializers.CharField())
    notes = serializers.CharField(allow_null=True)
    ocr_text = serializers.CharField()
    order_date = serializers.DateTimeField(allow_null=True)
    payment = serializers.DictField(child=serializers.CharField(), allow_null=True)
    pdf_url = serializers.CharField(allow_null=True)
    purchase_order_number = serializers.CharField(allow_null=True)
    reference_number = serializers.CharField()
    rounding = serializers.FloatField(allow_null=True)
    service_end_date = serializers.DateTimeField(allow_null=True)
    service_start_date = serializers.DateTimeField(allow_null=True)
    ship_date = serializers.DateTimeField(allow_null=True)
    ship_to = serializers.DictField(child=serializers.CharField(), allow_null=True)
    shipping = serializers.CharField(allow_null=True)
    store_number = serializers.IntegerField(allow_null=True)
    subtotal = serializers.FloatField()
    tags = serializers.ListField(child=serializers.CharField())
    tax = serializers.FloatField(allow_null=True)
    tax_lines = serializers.ListField(child=serializers.DictField(child=serializers.CharField()))
    tip = serializers.FloatField(allow_null=True)
    total = serializers.FloatField()
    total_weight = serializers.FloatField(allow_null=True)
    tracking_number = serializers.CharField(allow_null=True)
    updated_date = serializers.DateTimeField()
    vendor = serializers.DictField(child=serializers.CharField(), allow_null=True)

class ViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'

class inlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineItem
        fields = '__all__'

