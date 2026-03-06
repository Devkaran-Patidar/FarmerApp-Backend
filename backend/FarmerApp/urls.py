from django.urls import path
from . import views

urlpatterns = [
    #============= farmer =========
    path("addproduct/", views.add_product),
    path("editproduct/<id>/",views.Editproduct),
    path("deleteproduct/<id>/",views.Deleteproduct),
    path("myproduct/",views.Myproduct),

    # ======= buyer =============
    path("allproducts/",views.AllProducts),
     path("add-to-cart/", views.add_to_cart),
    path("view-cart/", views.view_cart),
    path("update-cart/<int:item_id>/", views.update_cart_item),
    path("remove-cart/<int:item_id>/", views.remove_cart_item),
    path("buy-now/", views.buy_now),
    path("orders/<int:order_id>/",views.get_order),
    path("myorders/", views.my_orders),
    path("create-order/", views.create_order),
    path("orders/", views.FarmerOrdersView),
    path("order-item/<int:item_id>/deliver/", views.mark_as_delivered),
    path("earning/", views.FarmerEarning),
    path("product/<int:product_id>/",views.product_details)
]
