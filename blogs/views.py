from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView, ListView

from blogs.forms import BlogCommentForm
from blogs.models import BlogPost
from home.views import TenantAccessPublicMixin


class BlogPostView(TenantAccessPublicMixin, DetailView):
    queryset = BlogPost.objects.all()
    template_name = 'blog-templates/default/single-post.html'
    context_object_name = 'post'

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


class BlogPostListView(TenantAccessPublicMixin, ListView):
    template_name = 'blog-templates/default/post-list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return BlogPost.objects.filter(site=self.request.tenant)
