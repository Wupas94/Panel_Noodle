from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, TimeEntry, Payout
from django.utils import timezone


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(TimeEntry)
class TimeEntryAdmin(admin.ModelAdmin):
    list_display = ('employee', 'start_time', 'end_time', 'duration', 'status', 'week_number', 'year')
    list_filter = ('status', 'employee__department', 'week_number', 'year')
    search_fields = ('employee__user__username', 'employee__user__first_name', 'employee__user__last_name', 'notes')
    readonly_fields = ('duration', 'week_number', 'year')
    ordering = ('-start_time',)
    date_hierarchy = 'start_time'

    def save_model(self, request, obj, form, change):
        if not change:  # Only for new objects
            obj.approved_by = request.user
            obj.approved_at = timezone.now()
        super().save_model(request, obj, form, change)


@admin.register(Payout)
class PayoutAdmin(admin.ModelAdmin):
    list_display = ('employee', 'period_start_date', 'period_end_date', 'total_pay', 'status')
    list_filter = ('status', 'employee__department', 'period_start_date')
    search_fields = ('employee__user__username', 'employee__user__first_name', 'employee__user__last_name', 'notes')
    readonly_fields = ('total_pay', 'calculated_at')
    ordering = ('-period_start_date',)
    date_hierarchy = 'period_start_date'

    fieldsets = (
        ('Informacje podstawowe', {
            'fields': ('employee', 'period_start_date', 'period_end_date', 'status')
        }),
        ('Godziny', {
            'fields': ('approved_hours', 'overtime_hours')
        }),
        ('Wynagrodzenie', {
            'fields': ('base_pay_earned', 'overtime_pay_earned', 'bonuses', 'deductions', 'total_pay')
        }),
        ('Daty i notatki', {
            'fields': ('calculated_at', 'paid_at', 'notes')
        }),
    )
