from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
# from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductsForm, VersionForm
from catalog.models import Products, Version


class ProductsListView(ListView):
    model = Products

    # def get_context_data(self, **kwargs):
    #     context_data = super().get_context_data(**kwargs)
    #     self.object.views_count += 1
    #     self.object.save()
    #     return self.object


class ProductsDetailView(DetailView):
    model = Products

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class ProductsCreateView(CreateView):
    model = Products
    # fields = ("name", "description", "price", "image", "category")
    form_class = ProductsForm
    success_url = reverse_lazy('products:products_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Products, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST)
        else:
            context_data['formset'] = VersionFormset()
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if form.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class ProductsUpdateView(UpdateView):
    model = Products
    # fields = ("name", "description", "price", "image", "category")
    form_class = ProductsForm
    success_url = reverse_lazy('products:products_list')

    def get_success_url(self):
        return reverse('products:products_detail', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Products, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class ProductsDeleteView(DeleteView):
    model = Products
    success_url = reverse_lazy('products:products_list')


class ContactsTemplateView(TemplateView):
    template_name = "catalog/contacts.html"
    extra_context_data = {"title": "Контакты"}

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = "Контакты"
    #     return context

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
