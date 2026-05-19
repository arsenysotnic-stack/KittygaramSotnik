from datetime import date
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from cats.models import Cat
from .filters import HealthRecordFilter
from .models import Clinic, HealthRecord
from .permissions import IsCatOwnerOrReadOnly
from .serializers import (
    ClinicSerializer, HealthRecordSerializer, HealthRecordCreateSerializer
)


class ClinicViewSet(viewsets.ModelViewSet):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'address']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class HealthRecordViewSet(viewsets.ModelViewSet):
    queryset = HealthRecord.objects.select_related(
        'cat', 'cat__owner', 'clinic', 'created_by'
    ).all()
    permission_classes = [IsCatOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = HealthRecordFilter
    search_fields = ['title', 'description', 'doctor_name', 'cat__name']
    ordering_fields = ['date', 'next_date', 'created_at']
    ordering = ['-date']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return HealthRecordCreateSerializer
        return HealthRecordSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def complete(self, request, pk=None):
        record = self.get_object()
        if record.cat.owner != request.user:
            return Response(
                {'detail': 'У вас нет прав для этого действия.'},
                status=status.HTTP_403_FORBIDDEN
            )
        if record.is_completed:
            return Response(
                {'detail': 'Запись уже отмечена как выполненная.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        record.is_completed = True
        record.save()
        return Response(
            HealthRecordSerializer(record, context={'request': request}).data
        )

    @action(detail=False, methods=['get'], url_path='cat/(?P<cat_id>[^/.]+)')
    def cat_records(self, request, cat_id=None):
        cat = get_object_or_404(Cat, id=cat_id)
        queryset = self.filter_queryset(self.get_queryset().filter(cat=cat))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = HealthRecordSerializer(
                page, many=True, context={'request': request}
            )
            return self.get_paginated_response(serializer.data)
        return Response(
            HealthRecordSerializer(queryset, many=True, context={'request': request}).data
        )

    @action(
        detail=False,
        methods=['get'],
        url_path='cat/(?P<cat_id>[^/.]+)/upcoming'
    )
    def upcoming(self, request, cat_id=None):
        cat = get_object_or_404(Cat, id=cat_id)
        queryset = self.get_queryset().filter(
            cat=cat,
            next_date__gte=date.today(),
            is_completed=False
        ).order_by('next_date')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = HealthRecordSerializer(
                page, many=True, context={'request': request}
            )
            return self.get_paginated_response(serializer.data)
        return Response(
            HealthRecordSerializer(queryset, many=True, context={'request': request}).data
        )

    @action(
        detail=False,
        methods=['get'],
        url_path='cat/(?P<cat_id>[^/.]+)/stats'
    )
    def stats(self, request, cat_id=None):
        cat = get_object_or_404(Cat, id=cat_id)
        records = HealthRecord.objects.filter(cat=cat)
        today = date.today()

        by_type_qs = records.values('record_type').annotate(count=Count('id'))
        type_labels = dict(HealthRecord.RECORD_TYPE_CHOICES)
        by_type = [
            {
                'record_type': row['record_type'],
                'record_type_display': type_labels.get(
                    row['record_type'], row['record_type']
                ),
                'count': row['count'],
            }
            for row in by_type_qs
        ]

        totals = records.aggregate(
            total=Count('id'),
            completed=Count('id', filter=Q(is_completed=True)),
            pending=Count('id', filter=Q(is_completed=False)),
            upcoming=Count(
                'id',
                filter=Q(is_completed=False, next_date__gte=today),
            ),
            overdue=Count(
                'id',
                filter=Q(is_completed=False, next_date__lt=today, next_date__isnull=False),
            ),
        )

        return Response({
            'cat_id': cat.id,
            'cat_name': cat.name,
            'total': totals['total'],
            'completed': totals['completed'],
            'pending': totals['pending'],
            'upcoming': totals['upcoming'],
            'overdue': totals['overdue'],
            'by_type': by_type,
        })
