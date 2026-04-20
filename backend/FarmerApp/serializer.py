from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import productModel ,ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ["id", "image_url"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        return obj.product_img.url if obj.product_img else None

class productSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True,)
    class Meta:
        model =productModel
        fields ='__all__'
        read_only_fields = ['farmer_id']


from .models import CartItem 
class CartItemSerializer(serializers.ModelSerializer):
    product = productSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']

