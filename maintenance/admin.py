from django.contrib import admin
from .models import Property, MaintenanceRequest, RequestComment

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'address', 'created_at']
    search_fields = ['title', 'address']
    ordering = ['id']


@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "property",
        "created_by",
        "category",
        "priority",
        "status",
        "created_at",
    ]
    list_filter = ["category", "priority", "status", "created_at"]
    search_fields = ["title", "description", "property__title", "created_by__username"]
    ordering = ["-created_at"]


@admin.register(RequestComment)
class RequestCommentAdmin(admin.ModelAdmin):
    list_display = ["id", "request", "author", "created_at"]
    search_fields = ["message", "request__title", "author__username"]
    ordering = ["-created_at"]
