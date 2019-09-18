from django.urls import path, reverse_lazy
from django.utils.translation import ugettext_lazy as _

from documents import public_views
from documents.forms import DocumentForm
from documents.models import Document
from users.views import MultiEntryDeleteView, MultiEntryUpdateView, MultiEntryView

app_name = 'docs_public'

urlpatterns = [
    path('', MultiEntryView.as_view(
        extra_context={'document': True, 'nav_section': 'document'},
        form_title=_('Manage Documents (e.g. CV, Certificates..)'),
        form_class=DocumentForm,
        success_url=reverse_lazy('docs_public:home'),
        add_item_title=_('Add Document'),
        inject_initial=['user'],
        model=Document,
        object_list_filter=['user']
    ), name='home'),
    path('<slug:slug>/update/', MultiEntryUpdateView.as_view(
        extra_context={'document': True, 'nav_section': 'document'},
        form_class=DocumentForm,
        success_url=reverse_lazy('docs_public:home'),
        model=Document,
    ), name='edit'),
    path('<slug:slug>/delete/', MultiEntryDeleteView.as_view(
        extra_context={'document': True, 'nav_section': 'document'},
        success_url=reverse_lazy('docs_public:home'),
        model=Document,
    ), name='delete'),
]
