from attr import fields
from rest_framework import serializers

from . import models


class CategorySerializer(serializers.ModelSerializer):
    """
        Category Serializer
    """
    class Meta(object):
        """
            Meta
        """
        model = models.Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    """
        Product Serializer
    """
    class Meta(object):
        """
            Meta
        """
        model = models.Product
        fields = "__all__"
