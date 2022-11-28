from unicodedata import name
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.index),
    path('add_product/',views.addProduct),
    path('add_product/process_add_product/',views.procesAddProduct, name="process_add_product"),
    path('login/',views.login),
    path('logout/',views.logout),
    path('managerProduct/',views.listProduct),
    path('managerStatisticalWeek/',views.statisticalWeek),
    path('managerStatisticalYear/',views.statisticalYear),
    path('managerCheckout/',views.managerCheckOut),
    path('managerCheckout/detailOrder/',views.viewDetailOrder),
    path('managerCheckout/actionOrder/',views.actionOrder,name="action_order"),
    path('managerProduct/deleteProduct/',views.processDelete),
    path('managerProduct/updateProduct/',views.UpdateProduct),
    path('managerProduct/updateProduct/processUpdate/',views.processUpdate,name="process_update_product"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)