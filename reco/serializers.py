from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    product_tags = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_product_tags(self, obj):
        return [tag.name for tag in obj.product_tags.all()]
