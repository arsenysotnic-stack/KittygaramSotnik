from rest_framework import serializers
from .models import Clinic, HealthRecord


class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = ('id', 'name', 'address', 'phone', 'website', 'created_at')
        read_only_fields = ('created_at',)


class HealthRecordSerializer(serializers.ModelSerializer):
    cat_name = serializers.CharField(source='cat.name', read_only=True)
    record_type_display = serializers.CharField(
        source='get_record_type_display', read_only=True
    )
    clinic_name = serializers.CharField(
        source='clinic.name', read_only=True, allow_null=True, default=None
    )
    created_by_username = serializers.CharField(
        source='created_by.username', read_only=True
    )

    class Meta:
        model = HealthRecord
        fields = (
            'id', 'cat', 'cat_name', 'record_type', 'record_type_display',
            'title', 'description', 'date', 'next_date',
            'clinic', 'clinic_name', 'doctor_name',
            'is_completed', 'created_by', 'created_by_username', 'created_at'
        )
        read_only_fields = ('created_by', 'created_at', 'is_completed')


class HealthRecordCreateSerializer(HealthRecordSerializer):
    def validate_cat(self, cat):
        request = self.context.get('request')
        if request and cat.owner != request.user:
            raise serializers.ValidationError(
                'Вы можете добавлять записи только для своих котиков.'
            )
        return cat

    def validate(self, data):
        date = data.get('date')
        next_date = data.get('next_date')
        if date and next_date and next_date <= date:
            raise serializers.ValidationError({
                'next_date': 'Дата следующей процедуры должна быть позже даты текущей.'
            })
        return data
