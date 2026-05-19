from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Cat, Achievement
from .serializers import CatSerializer, CatCreateUpdateSerializer, AchievementSerializer
from .permissions import IsOwnerOrReadOnly


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['color', 'birth_year']
    search_fields = ['name', 'owner__username']
    ordering_fields = ['name', 'birth_year', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CatCreateUpdateSerializer
        return CatSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_cats(self, request):
        cats = self.queryset.filter(owner=request.user)
        cats = self.filter_queryset(cats)
        page = self.paginate_queryset(cats)
        if page is not None:
            return self.get_paginated_response(
                self.get_serializer(page, many=True).data
            )
        return Response(self.get_serializer(cats, many=True).data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_achievement(self, request, pk=None):
        cat = self.get_object()
        achievement_id = request.data.get('achievement_id')
        if not achievement_id:
            return Response(
                {'error': 'achievement_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            achievement = Achievement.objects.get(id=achievement_id)
            cat.achievements.add(achievement)
            return Response(
                {'message': f'Achievement {achievement.name} added'},
                status=status.HTTP_200_OK
            )
        except Achievement.DoesNotExist:
            return Response(
                {'error': 'Achievement not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = ['name']
