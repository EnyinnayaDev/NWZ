from django.contrib import admin, messages

from .models import Appointment, ContactMessage, Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration_minutes', 'price', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'summary')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'service', 'date', 'time', 'mode', 'status_badge', 'created_at')
    list_filter = ('status', 'mode', 'service')
    search_fields = ('full_name', 'email', 'phone')
    date_hierarchy = 'date'
    readonly_fields = ('created_at', 'updated_at')

    actions = ['mark_confirmed', 'mark_completed', 'mark_cancelled']

    def status_badge(self, obj):
        return obj.get_status_display()
    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'status'

    def get_readonly_fields(self, request, obj=None):
        readonly = list(self.readonly_fields)
        if obj and obj.status in Appointment.LOCKED_STATUSES:
            readonly.append('status')
        return readonly

    def save_model(self, request, obj, form, change):
        obj.full_clean()
        super().save_model(request, obj, form, change)

    def _bulk_set_status(self, request, queryset, new_status, label):
        updated, skipped = 0, 0
        for appt in queryset:
            if appt.status in Appointment.LOCKED_STATUSES:
                skipped += 1
                continue
            appt.status = new_status
            appt.save()
            updated += 1
        if updated:
            self.message_user(request, f"{updated} appointment(s) marked as {label}.", messages.SUCCESS)
        if skipped:
            self.message_user(
                request,
                f"{skipped} appointment(s) were already cancelled/completed and were left unchanged.",
                messages.WARNING,
            )

    def mark_confirmed(self, request, queryset):
        self._bulk_set_status(request, queryset, 'confirmed', 'confirmed')
    mark_confirmed.short_description = "Mark selected as Confirmed"

    def mark_completed(self, request, queryset):
        self._bulk_set_status(request, queryset, 'completed', 'completed')
    mark_completed.short_description = "Mark selected as Completed"

    def mark_cancelled(self, request, queryset):
        self._bulk_set_status(request, queryset, 'cancelled', 'cancelled')
    mark_cancelled.short_description = "Mark selected as Cancelled"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read',)
    list_editable = ('is_read',)
    search_fields = ('name', 'email', 'message')