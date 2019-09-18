from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import DetailView, ListView, TemplateView

from blogs.forms import BlogCommentForm
from blogs.models import BlogPost, SiteBlogTemplate, BlogCategory
from home.views import TenantAccessPublicMixin
from users.forms import ContactDataForm


class TemplateSelector:
    template_file_name = ''

    def get_context_data(self, **kwargs):
        ctx = super(TemplateSelector, self).get_context_data(**kwargs)
        ctx['categories'] = BlogCategory.objects.filter(site=self.request.tenant)
        return ctx

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
    template_file_name = 'single.html'
    extra_context = {'is_home_tab': True, 'is_single_post': True}

    def get_context_data(self, **kwargs):
        ctx = super(BlogPostView, self).get_context_data(**kwargs)
        ctx['comment_form'] = BlogCommentForm(initial={'post': self.get_object().id})
        ctx['related'] = BlogPost.objects.filter(site=self.request.tenant).exclude(pk=self.get_object().id)
        return ctx

    def dispatch(self, request, *args, **kwargs):
        response = super(BlogPostView, self).dispatch(request, *args, **kwargs)
        post = self.get_object()
        ss_key = 'has_read_' + str(post.id)
        if not self.request.session.get(ss_key):
            self.request.session[ss_key] = True
            post.views += 1
            post.save()
        return response

    def post(self, request, *args, **kwargs):
        comment_parent_id = request.POST.get('parent_id')
        form = BlogCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            if comment_parent_id:
                comment.parent_id = comment_parent_id
            comment.save()
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
    extra_context = {'is_home_tab': True}
    paginate_by = 25

    def get_context(self, **kwargs):
        ctx = super(BlogPostListView, self).get_context_data(**kwargs)
        featured = self.get_queryset().filter(is_featured=True)
        ctx['featured'] = featured
        ctx['total_posts'] = self.get_queryset().count()
        return ctx

    def get_queryset(self):
        return BlogPost.objects.filter(site=self.request.tenant)


class BlogTestView(TenantAccessPublicMixin, TemplateSelector, TemplateView):
    template_file_name = 'index.html'


class BlogCategoryView(TenantAccessPublicMixin, TemplateSelector, ListView):
    template_file_name = 'category.html'
    extra_context = {'is_category_tab': True}
    paginate_by = 30
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        ctx = super(BlogCategoryView, self).get_context_data(**kwargs)
        ctx['category'] = get_object_or_404(BlogCategory, pk=self.kwargs.get('pk'))
        return ctx

    def get_queryset(self):
        return BlogPost.objects.filter(site=self.request.tenant, category_id=self.kwargs.get('pk'))


class BlogCategoriesView(TenantAccessPublicMixin, TemplateSelector, ListView):
    template_file_name = 'category-list.html'
    extra_context = {'is_category_tab': True}
    context_object_name = 'posts'

    def get_queryset(self):
        return BlogCategory.objects.filter(site=self.request.tenant)


class BlogArchivesView(TenantAccessPublicMixin, TemplateSelector, ListView):
    template_file_name = 'archive.html'
    extra_context = {'is_archive_tab': True}
    paginate_by = 30
    context_object_name = 'posts'

    def get_queryset(self):
        posts = BlogPost.objects.filter(site=self.request.tenant)
        search = self.request.GET.get('search')
        if search:
            posts = posts.filter(Q(title__icontains=search) | Q(content__icontains=search))
        return posts


class BlogContactView(TenantAccessPublicMixin, TemplateSelector, TemplateView):
    template_file_name = 'contact.html'
    extra_context = {'is_contact_tab': True}

    def get_context_data(self, **kwargs):
        ctx = super(BlogContactView, self).get_context_data(**kwargs)
        ctx['contact_form'] = ContactDataForm(initial={'client': self.request.tenant.id})
        return ctx
