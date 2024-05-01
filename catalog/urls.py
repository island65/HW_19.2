from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from catalog.views import products_list, products_specifications
from catalog.apps import CatalogConfig

# from catalog.views import contacts

app_name = CatalogConfig.name

urlpatterns = [
    path('', products_list, name='products_list'),
    path('products/<int:pk>/', products_specifications, name='products_specs'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns = [
#     path('', home),
#     path('contacts/', contacts)
