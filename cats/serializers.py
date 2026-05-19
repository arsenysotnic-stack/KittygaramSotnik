import base64
from django.core.files.base import ContentFile
from rest_framework import serializers
from .models import Cat, Achievement, AchievementCat


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'temp.{ext}')
        return super().to_internal_value(data)


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ('id', 'name')


class CatSerializer(serializers.ModelSerializer):
    achievements = AchievementSerializer(many=True, read_only=True)
    image = Base64ImageField(required=False, allow_null=True)
    age = serializers.SerializerMethodField()

    class Meta:
        model = Cat
        fields = (
            'id', 'name', 'color', 'birth_year', 'image',
            'owner', 'achievements', 'age', 'created_at'
        )
        read_only_fields = ('owner', 'created_at')

    def get_age(self, obj):
        from datetime import datetime
        return datetime.now().year - obj.birth_year

    def validate_birth_year(self, value):
        from datetime import datetime
        current_year = datetime.now().year
        if value < 1900:
            raise serializers.ValidationError('Год рождения не может быть раньше 1900')
        if value > current_year:
            raise serializers.ValidationError('Год рождения не может быть в будущем')
        return value


class CatCreateUpdateSerializer(CatSerializer):
    achievements = AchievementSerializer(many=True, read_only=True)
    achievement_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        queryset=Achievement.objects.all(),
        required=False
    )

    class Meta(CatSerializer.Meta):
        fields = CatSerializer.Meta.fields + ('achievement_ids',)

    def create(self, validated_data):
        achievements = validated_data.pop('achievement_ids', [])
        cat = Cat.objects.create(**validated_data)
        for achievement in achievements:
            AchievementCat.objects.create(cat=cat, achievement=achievement)
        return cat

    def update(self, instance, validated_data):
        achievements = validated_data.pop('achievement_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if achievements is not None:
            AchievementCat.objects.filter(cat=instance).delete()
            for achievement in achievements:
                AchievementCat.objects.create(cat=instance, achievement=achievement)
        return instance
