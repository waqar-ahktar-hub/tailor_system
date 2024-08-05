"""urls for product application."""

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from product.views.product_images_views import product_images_add_view, product_images_update_view
from product.views.product_views import (
    product_add_view,
    product_delete_view,
    product_detail_view,
    product_list_view,
    product_update_view
)

app_name = 'product'

urlpatterns = [
    path('products/', product_list_view, name='products'),
    path('product/<int:id>/', product_detail_view, name='product_detail'),
    path('product/add/', product_add_view, name='product_add'),
    path('product/update/<int:id>/', product_update_view, name='product_update'),
    path('product/delete/', product_delete_view, name='product_delete'),

    path('product_images/add/<int:product_id>/', product_images_add_view, name='product_images_add'),
    path('product_images/update/<int:product_id>/', product_images_update_view, name='product_images_update'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
