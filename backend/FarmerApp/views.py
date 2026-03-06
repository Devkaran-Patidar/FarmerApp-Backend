from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import productModel
from .serializer import productSerializer
from .models import ProductImage
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_product(request):
    serializer = productSerializer(data=request.data)

    if serializer.is_valid():
        product = serializer.save(farmer_id=request.user)

        images = request.FILES.getlist("product_img")

        # Optional limit
        if len(images) > 5:
            return Response(
                {"message": "Maximum 5 images allowed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        for image in images:
            ProductImage.objects.create(
                product=product,
                product_img=image
            )

        # 🔥 Return product with images
        final_serializer = productSerializer(
            product,
            context={"request": request}
        )

        return Response(final_serializer.data, status=201)

    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Myproduct(request):

    products = productModel.objects.filter(farmer_id=request.user)

    serializer = productSerializer(products, many=True,context={"request": request})
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def Deleteproduct(request, id):

    try:
        product = productModel.objects.get(id=id, farmer_id=request.user)
    except productModel.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)

    product.delete()

    return Response({"message": "Product deleted successfully"})


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def Editproduct(request, id):

    try:
        product = productModel.objects.get(id=id, farmer_id=request.user)
    except productModel.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)

    serializer = productSerializer(
        product,
        data=request.data,
        partial=True,
        context={"request": request}
    )

    if serializer.is_valid():
        serializer.save()

        # ✅ Handle multiple images
        images = request.FILES.getlist("images")

        if images:
            # Optional: delete old images
            ProductImage.objects.filter(product=product).delete()

            for img in images:
                ProductImage.objects.create(
                    product=product,
                    product_img=img
                )

        return Response(
            productSerializer(product, context={"request": request}).data
        )

    return Response(serializer.errors, status=400)

# -------------------------buyer---------------


from rest_framework.permissions import AllowAny
from django.db.models import Q

@api_view(['GET'])
@permission_classes([AllowAny])
def AllProducts(request):
    search = request.GET.get('search', '')
    category = request.GET.get('category', '')

    qs = productModel.objects.all()

    # search filter
    if search:
        qs = qs.filter(
            Q(name__icontains=search) |
            Q(category__icontains=search)
        )

    # category filter
    if category:
        qs = qs.filter(category__iexact=category)

    qs = qs.order_by('?')

    serializer = productSerializer(qs, many=True, context={'request': request})
    return Response(serializer.data)


from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import Cart, CartItem, productModel
from .serializer import CartItemSerializer
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def add_to_cart(request):
    product_id = request.data.get("product_id")
    quantity = int(request.data.get("quantity", 1))

    product = get_object_or_404(productModel, id=product_id)

    if product.available_quantity < quantity:
        return Response({"error": "Not enough stock"}, status=400)

    cart, _ = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity

    cart_item.save()

    return Response({"message": "Product added to cart"})




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    serializer = CartItemSerializer(items, many=True)
    total_price = 0
    for item in items:
        total_price += item.product.price_per_unit * item.quantity
    return Response({
    "success": True,
    "items": serializer.data,
    "cart_total": total_price,
    "cart_count": items.count()
})


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_cart_item(request, item_id):
    quantity = int(request.data.get("quantity", 1))

    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

    if cart_item.product.available_quantity < quantity:
        return Response({"error": "Not enough stock"}, status=400)

    cart_item.quantity = quantity
    cart_item.save()

    return Response({"message": "Cart updated"})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_cart_item(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

    cart_item.delete()

    return Response({"message": "Item removed from cart"})


from .models import Order, OrderItem

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def buy_now(request):
    product_id = request.data.get("product_id")
    quantity = int(request.data.get("quantity", 1))

    product = get_object_or_404(productModel, id=product_id)

    if product.available_quantity < quantity:
        return Response({"error": "Not enough stock"}, status=400)

    # Reduce stock immediately
    product.available_quantity -= quantity
    product.save()

    total_price = product.price_per_unit * quantity

     # Save order
    order = Order.objects.create(user=request.user, total_price=total_price)
    OrderItem.objects.create(
        order=order,
        product=product,
        quantity=quantity,
        price=product.price_per_unit
    )

     # Remove item from user's cart if exists
    try:
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.delete()
    except (Cart.DoesNotExist, CartItem.DoesNotExist):
        pass  # if cart or item doesn't exist, ignore

    return Response({
        "message": "Purchase successful",
        "order_id": order.id,
        "product": product.name,
        "quantity": quantity,
        "total_price": total_price
    })

# receipt

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = [
        {
            "product": item.product.name,
            "quantity": item.quantity,
            "price": item.price,
        } for item in order.items.all()
    ]
    return Response({
        "order_id": order.id,
        "total_price": order.total_price,
        "created_at": order.created_at,
        "items": items
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    data = []
    for order in orders:
        items = [
            {
                "product": item.product.name,
                "quantity": item.quantity,
                "price": item.price
            } for item in order.items.all()
        ]
        data.append({
            "order_id": order.id,
            "total_price": order.total_price,
            "created_at": order.created_at,
            "items": items
        })
    return Response(data)



# receipt
from django.db import transaction

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def create_order(request):
    items = request.data.get("items", [])
    total = request.data.get("total")

    if not items:
        return Response({"error": "No items provided"}, status=400)

    order = Order.objects.create(
        user=request.user,
        total_price=total
    )

    for item in items:
        product_id = item["product"]["id"]
        quantity = int(item["quantity"])

        product = get_object_or_404(productModel, id=product_id)

        # ✅ Check stock
        if product.available_quantity < quantity:
            return Response(
                {"error": f"Not enough stock for {product.name}"},
                status=400
            )

        # ✅ Reduce stock
        product.available_quantity -= quantity
        product.save()

        # ✅ Create order item
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price_per_unit
        )

        # ✅ Remove from cart
        try:
            cart = Cart.objects.get(user=request.user)
            CartItem.objects.filter(cart=cart, product=product).delete()
        except Cart.DoesNotExist:
            pass

    return Response({
        "message": "Order created successfully",
        "order_id": order.id
    })


# farmer order history
from rest_framework.views import APIView
from .models import OrderItem
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def FarmerOrdersView(request):
        farmer = request.user

        order_items = OrderItem.objects.filter(
            product__farmer_id=farmer
        ).select_related("order", "product")

        data = []

        for item in order_items:
            data.append({
                 "id": item.id,
                "order_id": item.order.id,
                "email":item.order.user.email,
                "product_name": item.product.name,
                "total_ammount":item.order.total_price,
                "quantity": item.quantity,
                "price": item.price,
                "buyer": item.order.user.username,
                "created_at": item.order.created_at,
            })

        return Response(data)


# order deliver


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def mark_as_delivered(request, item_id):

    try:
        item = OrderItem.objects.get(
            id=item_id,
            product__farmer_id=request.user
        )

        item.status = "Delivered"
        item.save()

        return Response({"message": "Marked as Delivered"})

    except OrderItem.DoesNotExist:
        return Response({"error": "Not allowed"}, status=403)
    

# earning of farmer
from django.db.models import F, Sum, DecimalField, ExpressionWrapper
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def FarmerEarning(request):

    farmer = request.user

    total = OrderItem.objects.filter(
        product__farmer_id=farmer,
        # status="Delivered"
    ).aggregate(
        total_earning=Sum(F('price') * F('quantity'))
    )

    return Response({
        "total_earning": total["total_earning"] or 0,
        "delivered_orders": OrderItem.objects.filter(
        product__farmer_id=request.user,
        # status="Delivered"
    ).count()
    })




# @api_view(['GET'])
# def ProductDetails(req ,product_id):
from rest_framework import status
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product_details(request, product_id):
    try:
        product = productModel.objects.get(id=product_id)
    except productModel.DoesNotExist:
        return Response(
            {"error": "Product not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = productSerializer(product, context={"request": request})

    return Response({
        "success": True,
        "product": serializer.data,
    })