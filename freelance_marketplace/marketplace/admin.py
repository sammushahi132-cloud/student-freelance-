"""
Django Admin Configuration for Student Freelance Marketplace
Registers Profile, Project, and Proposal models with list_display, search_fields, and list_filter.
"""

from django.contrib import admin
from .models import Profile, Project, Proposal


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'education', 'get_email')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email', 'skills', 'education')

    @admin.display(description='Email')
    def get_email(self, obj):
        return obj.user.email


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'category', 'budget', 'deadline', 'status', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'description', 'client__username', 'client__email')
    list_editable = ('status',)
    date_hierarchy = 'created_at'


@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ('project', 'student', 'proposed_amount', 'estimated_days', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('project__title', 'student__username', 'student__email', 'description')
    list_editable = ('status',)
    date_hierarchy = 'created_at'
