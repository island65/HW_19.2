from django.shortcuts import render, get_object_or_404

from catalog.models import Products


def products_list(request):
    products = Products.objects.all()
    context = {"products": products}
    return render(request, 'catalog/products_list.html', context)


def products_specifications(request, pk):
    product = get_object_or_404(Products, pk=pk)
    context = {"product": product}
    return render(request, 'catalog/products_specs.html', context)


# Code to Home_Work_19.2
# def home(request):
#     return render(request, 'catalog/home.html')
#
#
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
