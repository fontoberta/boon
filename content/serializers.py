import os
from rest_framework import serializers

from django.contrib.auth.models import Group

from .models import Project
from .models import Section
from .models import ImageContent

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')

class BaseSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='created_by.username'
    )
    class Meta:
        abstract = True

class ProjectSerializer(BaseSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'slug',
                  'description', 'created_by')

class SectionSerializer(BaseSerializer):
    project = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='project.slug'
    )
    class Meta:
        model = Section
        fields = ('id', 'project', 'name', 'slug', 'is_gallery', 'created_by')

class ImageContentSerializer(BaseSerializer):
    section = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='section.slug'
    )
    class Meta:
        model = ImageContent
        fields = ('id', 'section', 'name', 'slug', 'image', 'created_by')

    def update(self, instance, validated_data):
        if instance.image.path.rsplit('/', 1)[1] != \
            validated_data['image'].name:
            os.remove(instance.image.path)
        instance.image.save(validated_data['image'].name,
                            validated_data['image'])
        instance.save()
        return instance
