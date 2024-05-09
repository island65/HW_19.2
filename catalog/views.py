from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.models import Products


class ProductsListView(ListView):
    model = Products


class ProductsDetailView(DetailView):
    model = Products

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class ProductsCreateView(CreateView):
    model = Products
    fields = ("name", "description", "price", "image", "category")
    success_url = reverse_lazy('products:products_list')


class ProductsUpdateView(UpdateView):
    model = Products
    fields = ("name", "description", "price", "image", "category")
    success_url = reverse_lazy('products:products_list')

    def get_success_url(self):
        return reverse('products:products_detail', args=[self.kwargs.get('pk')])


class ProductsDeleteView(DeleteView):
    model = Products
    success_url = reverse_lazy('products:products_list')


class ContactsTemplateView(TemplateView):
    template_name = "catalog/contacts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Контакты"
        return context

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Имя: {name} \nТелефон: {phone} \nСообщение: {message}')
        return HttpResponseRedirect(reverse('catalog:contacts'))


# def products_list(request):
#     products = Products.objects.all()
#     context = {"products": products}
#     return render(request, 'catalog/products_list.html', context)


# def products_specifications(request, pk):
#     product = get_object_or_404(Products, pk=pk)
#     context = {"product": product}
#     return render(request, 'catalog/products_detail.html', context)

# class HomeListView(ListView):
#     model = Products


# def home(request):
#     return render(request, 'catalog/home.html')


# def contacts(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         phone = request.POST.get('phone')
#         message = request.POST.get('message')
#         print(f'Ваше сообщение: {name}, {phone}, {message}')
#         with open('write.txt', 'wt', encoding='UTF-8') as file:
#             file.write(f'Ваше сообщение: {name}, {phone}, {message}')
#
#     return render(request, 'catalog/contacts.html')
