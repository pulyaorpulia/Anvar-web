from django.contrib import admin
from .models import Contact, SiteSettings, TeamMember, Achievement, Partner


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['phone', 'email', 'address']


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'order']
    list_editable = ['order']


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['number', 'label', 'order']
    list_editable = ['order']


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    list_editable = ['order']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'is_read', 'created_at']
    list_editable = ['is_read']
    readonly_fields = ['name', 'email', 'phone', 'message', 'created_at']