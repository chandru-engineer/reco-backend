from django.db import models

# Create your models here.
class Product(models.Model):
    product_code = models.CharField(max_length=100, unique=True)
    product_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    product_tags = models.ManyToManyField('ProductTag', blank=True)
    preview_image_url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.product_name


class ProductTag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name