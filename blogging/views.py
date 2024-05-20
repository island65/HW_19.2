from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


from blogging.models import Blog


class BlogListView(ListView):
    model = Blog


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogCreateView(CreateView):
    model = Blog
    fields = ('title', 'body', 'image',)
    success_url = reverse_lazy('blogging:list')

    def form_valid(self, form):
        new_blog = form.save(commit=False)
        new_blog.slug = slugify(new_blog.title)
        new_blog.save()

        return super().form_valid(form)


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('title', 'body', 'image',)

    def form_valid(self, form):
        new_blog = form.save(commit=False)
        new_blog.slug = slugify(new_blog.title)
        new_blog.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blogging:detail', args=[self.kwargs.get('pk')])


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blogging:list')
