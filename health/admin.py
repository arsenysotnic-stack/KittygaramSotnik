from django.contrib import admin
from .models import Clinic, HealthRecord


@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'created_at')
    search_fields = ('name', 'address')
    ordering = ('name',)


@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'cat', 'record_type', 'title', 'date',
        'next_date', 'is_completed', 'created_by'
    )
    list_filter = ('record_type', 'is_completed', 'date')
    search_fields = ('title', 'description', 'cat__name', 'doctor_name')
    raw_id_fields = ('cat', 'clinic', 'created_by')
