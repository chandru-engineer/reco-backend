from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Product
from .serializers import ProductSerializer
from rest_framework.pagination import PageNumberPagination
    
import base64
from io import BytesIO
from PIL import Image

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Product
from .serializers import ProductSerializer
from .ml_model import detect_product



# Create your views here.
class ActiveProductsPagination(PageNumberPagination):
    page_size = 10  # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100




class ActiveProductsView(APIView):
    permission_classes = [AllowAny]
    pagination_class = ActiveProductsPagination

    def get(self, request, *args, **kwargs):
        active_products = Product.objects.filter(is_active=True).order_by('id')
        paginator = self.pagination_class()
        paginated_products = paginator.paginate_queryset(active_products, request)
        serializer = ProductSerializer(paginated_products, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            image_base64 = request.data.get("image")

            if not image_base64:
                return Response({"error": "No image data provided"}, status=status.HTTP_400_BAD_REQUEST)

            # If there's a data URL prefix, remove it
            if "base64," in image_base64:
                image_base64 = image_base64.split("base64,")[1]

            # Fix missing padding
            missing_padding = len(image_base64) % 4
            if missing_padding:
                image_base64 += '=' * (4 - missing_padding)

            # Decode the base64 image
            image_data = base64.b64decode(image_base64)
            image = Image.open(BytesIO(image_data))

            # Detect products using YOLO
            detected_labels = detect_product(image)

            print(detected_labels, 'detected_labels')

            # Recommend products based on detected labels
            recommended_products = Product.objects.filter(product_name__icontains=detected_labels[0]) if detected_labels else []

            serializer = ProductSerializer(recommended_products, many=True)
            return Response({
                "detected_labels": detected_labels,
                "recommendations": serializer.data
            })

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)