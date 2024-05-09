from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from catalog.views import ProductsListView, ProductsDetailView, ContactsTemplateView, ProductsCreateView, \
    ProductsUpdateView, ProductsDeleteView
from catalog.apps import CatalogConfig

# from catalog.views import contacts

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductsListView.as_view(), name='products_list'),
    path('products/<int:pk>/', ProductsDetailView.as_view(), name='products_detail'),
    path('products/create', ProductsCreateView.as_view(), name='products_create'),
    path('products/<int:pk>/update/', ProductsUpdateView.as_view(), name='products_update'),
    path('products/<int:pk>/delete/', ProductsDeleteView.as_view(), name='products_delete'),
    path('contacts/', ContactsTemplateView.as_view(), name='contacts')
]

# urlpatterns = [
#     path('', home),
#     path('contacts/', contacts)
