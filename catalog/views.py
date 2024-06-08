from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductsForm, VersionForm, ProductsModeratorForm
from catalog.models import Products, Version
from catalog.services import get_category_from_cache, get_products_from_cache


class ProductsListView(LoginRequiredMixin, ListView):
    model = Products

    def get_queryset(self, *args, **kwargs):
        queryset = get_products_from_cache()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset



    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        active_versions = []
        for product in self.get_queryset():
            version = product.version.filter(version_is_active=True).first()
            active_versions.append(version)
        context_data["versions"] = active_versions
        context_data["categories"] = get_category_from_cache()
        return context_data

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


class ProductsCreateView(LoginRequiredMixin, CreateView):
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
        if form.is_valid:
            new_object = form.save(commit=False)
            new_object.author = self.request.user
            new_object.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class ProductsUpdateView(LoginRequiredMixin, UpdateView):
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
        context_data = self.get_context_data()
        formset = context_data['formset']
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def get_form_class(self):
        user = self.request.user
        if user == self.object.user or user.is_superuser:
            return ProductsForm
        if (user.has_perm('catalog.set_published_status') and user.has_perm('catalog.change_description') and
                user.has_perm('catalog.change_category')):
            return ProductsModeratorForm
        raise PermissionDenied


class ProductsDeleteView(LoginRequiredMixin, DeleteView):
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
        if request.method == 'POST':
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            message = request.POST.get('message')
            print(f'Имя: {name} \nТелефон: {phone} \nСообщение: {message}')
        return render(request, self.template_name)

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
