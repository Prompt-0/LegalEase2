from django.contrib import admin
from .models import OnlineFIR, AnonymousReport, ContactMessage

@admin.register(OnlineFIR)
class OnlineFIRAdmin(admin.ModelAdmin):
    list_display = ('subject', 'complainant_name', 'district', 'status', 'created_at')
    list_filter = ('status', 'district', 'created_at')
    search_fields = ('subject', 'complainant_name', 'details')
    readonly_fields = ('created_at', 'user') # Admin can't change who submitted it

@admin.register(AnonymousReport)
class AnonymousReportAdmin(admin.ModelAdmin):
    list_display = ('incident_type', 'location', 'status', 'created_at')
    list_filter = ('status', 'incident_type', 'created_at')
    search_fields = ('location', 'description')
    readonly_fields = ('created_at', 'user')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'email', 'created_at')
    search_fields = ('subject', 'name', 'email', 'message')
    readonly_fields = ('created_at',)
