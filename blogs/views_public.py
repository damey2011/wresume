from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView
from django.utils.translation import ugettext as __

from blogs.forms import BlogPostForm, BlogCategoryForm
from blogs.models import BlogPost, BlogCategory
from wresume.utils import SiteAwareView


class BlogPostsView(LoginRequiredMixin, SiteAwareView, ListView):
    template_name = 'blogs/manager/post-list.html'
    extra_context = {'is_blog_posts': True, 'nav_section': 'blog'}
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return BlogPost.objects.filter(site=self.get_site())


class BlogCategoriesView(LoginRequiredMixin, SiteAwareView, ListView):
    template_name = 'blogs/manager/categories.html'
    extra_context = {'is_categories': True, 'nav_section': 'blog'}
    context_object_name = 'categories'

    def get_queryset(self):
        return BlogCategory.objects.filter(site=self.get_site())


class BlogCategoryDeleteView(LoginRequiredMixin, SuccessMessageMixin, View):
    success_url = reverse_lazy('blogs_public:categories')

    def get_success_message(self, cleaned_data):
        return __('{} has been deleted successfully'.format(cleaned_data['category']))

    def get(self, request, **kwargs):
        cat = get_object_or_404(BlogCategory, pk=kwargs.get('pk'))
        cat.delete()
        messages.success(request, self.get_success_message({'category': cat.category}))
        return HttpResponseRedirect(self.success_url)


class WritePostView(LoginRequiredMixin, SuccessMessageMixin, SiteAwareView, CreateView):
    template_name = 'blogs/manager/write.html'
    extra_context = {'is_write': True, 'nav_section': 'blog'}
    form_class = BlogPostForm
    success_url = reverse_lazy('blogs_public:write')

    def get_initial(self):
        init = super(WritePostView, self).get_initial()
        init['author'] = self.request.user.id
        init['site'] = self.get_site().id
        return init

    def get_success_message(self, cleaned_data):
        return __('{} has been created'.format(cleaned_data['title']))

    def get_queryset(self):
        return BlogPost.objects.filter(site=self.get_site())


class CreateCategoryView(LoginRequiredMixin, SuccessMessageMixin, SiteAwareView, CreateView):
    template_name = 'blogs/manager/create-category.html'
    extra_context = {'is_create_category': True, 'nav_section': 'blog'}
    form_class = BlogCategoryForm
    success_url = reverse_lazy('blogs_public:create-categories')

    def get_initial(self):
        init = super(CreateCategoryView, self).get_initial()
        init['site'] = self.get_site().id
        return init

    def get_success_message(self, cleaned_data):
        return __('{} has been created'.format(cleaned_data['category']))

    def get_queryset(self):
        return BlogCategory.objects.filter(site=self.get_site())
