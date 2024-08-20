from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from .models import HelpTopic, HelpCategory, Feedback
from django.db.models import Q

class HelpListView(ListView):
    model = HelpTopic
    template_name = 'help/help_list.html'
    context_object_name = 'help_topics'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = HelpCategory.objects.all()
        return context

class HelpDetailView(DetailView):
    model = HelpTopic
    template_name = 'help/help_detail.html'
    context_object_name = 'help_topic'

class HelpSearchView(ListView):
    model = HelpTopic
    template_name = 'help/help_search.html'
    context_object_name = 'search_results'

    def get_queryset(self):
        query = self.request.GET.get('q')
        category_id = self.request.GET.get('category')
        sort_by = self.request.GET.get('sort_by')

        queryset = HelpTopic.objects.all()

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
        
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if sort_by:
            queryset = queryset.order_by(sort_by)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = HelpCategory.objects.all()
        context['sort_options'] = [
            ('created_at', 'Date Created'),
            ('title', 'Title'),
        ]
        return context

def submit_feedback(request):
    if request.method == 'POST':
        help_topic_id = request.POST.get('help_topic_id')
        feedback_text = request.POST.get('feedback')

        if help_topic_id and feedback_text:
            help_topic = HelpTopic.objects.get(pk=help_topic_id)
            Feedback.objects.create(help_topic=help_topic, feedback=feedback_text)

    return redirect('help:help_index')
