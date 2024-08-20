from django.contrib import admin
from .models import HelpTopic, HelpCategory, Feedback

@admin.register(HelpCategory)
class HelpCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(HelpTopic)
class HelpTopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('category',)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('help_topic', 'created_at')
    search_fields = ('feedback',)
