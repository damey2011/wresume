from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView, ListView, TemplateView

from blogs.forms import BlogCommentForm
from blogs.models import BlogPost, SiteBlogTemplate, BlogCategory
from home.views import TenantAccessPublicMixin


class TemplateSelector:
    template_file_name = ''

    def template_prefix(self):
        ts = SiteBlogTemplate.objects.filter(client=self.request.tenant)
        if ts.exists():
            return ts.first().template.template_folder
        return SiteBlogTemplate.objects.order_by('created').first().template.template_folder

    def get_template_names(self):
        return [self.template_prefix() + self.template_file_name]


class BlogPostView(TenantAccessPublicMixin, TemplateSelector, DetailView):
    queryset = BlogPost.objects.all()
    context_object_name = 'post'
    template_file_name = 'index.html'

    def get_context_data(self, **kwargs):
        ctx = super(BlogPostView, self).get_context_data(**kwargs)
        ctx['comment_form'] = BlogCommentForm(initial={'post': self.get_object().id})
        return ctx

    def post(self, request, *args, **kwargs):
        form = BlogCommentForm(request.POST)
        if form.is_valid():
            form.save()
            # messages.success(request, 'Your comment was added', 'success')
            return HttpResponseRedirect(request.get_full_path())
        if 'is_ajax' in request.POST:
            return JsonResponse(form.errors, status=400)
        ctx = self.get_context_data()
        ctx['comment_form'] = form
        return render(request, self.template_name, ctx)


class BlogPostListView(TenantAccessPublicMixin, TemplateSelector, ListView):
    # template_name = 'blog-templates/default/post-list.html'
    template_file_name = 'index.html'
    context_object_name = 'posts'

    def get_context(self, **kwargs):
        ctx = super(BlogPostListView, self).get_context_data(**kwargs)
        ctx['featured'] = self.get_queryset().filter(is_featured=True)
        return ctx

    def get_queryset(self):
        return BlogPost.objects.filter(site=self.request.tenant)


class BlogTestView(TenantAccessPublicMixin, TemplateSelector, TemplateView):
    template_file_name = 'index.html'


class BlogCategoryView(TenantAccessPublicMixin, TemplateSelector, ListView):
    template_file_name = 'category.html'

    def get_queryset(self):
        return BlogPost.objects.filter(site=self.request.tenant)


class BlogCategoriesView(TenantAccessPublicMixin, TemplateSelector, ListView):
    template_file_name = 'category-list.html'

    def get_queryset(self):
        return BlogCategory.objects.filter(site=self.request.tenant)


class BlogArchivesView(TenantAccessPublicMixin, TemplateSelector, ListView):
    template_file_name = 'archive.html'

    def get_queryset(self):
        return BlogPost.objects.filter(site=self.request.tenant)
