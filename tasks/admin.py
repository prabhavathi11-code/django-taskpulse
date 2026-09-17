from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'priority', 'status', 'due_date', 'created_at')
    list_editable = ('status', 'priority')
    list_filter = ('status', 'priority', 'category', 'due_date')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)

