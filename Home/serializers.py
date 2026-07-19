from rest_framework import serializers
from .models import Contact
#from .models import Product

# class ProductSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Product
#         fields = "__all__"

class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = "__all__"