from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.index),
    path('login/',views.login),
    path('signup/',views.signup),
    path('shop/',views.shop),
    path('logout/',views.logout),
    path('shop/product-detail/',views.productDetail),
    path('shop/addToCart/',views.addToCart,name="add_cart"),
    path('shop/viewcart/',views.viewCart),
    path('shop/info/',views.info),
    path('shop/viewReceipt/',views.viewReceipt),
    path('shop/viewReceipt/detailOrder/',views.viewDetailOrder),
    path('shop/viewcart/changeQuantity',views.changeQuantity, name="change_quantity"),
    path('shop/viewcart/deleteInCart',views.deleteInCart, name="delete_in_cart"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)