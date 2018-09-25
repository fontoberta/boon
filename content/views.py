# pylint: disable=W0613
import os
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import Group

from rest_framework_extensions.mixins import NestedViewSetMixin

from .models import Project
from .models import Section
from .models import ImageContent

from .serializers import GroupSerializer
from .serializers import ProjectSerializer
from .serializers import SectionSerializer
from .serializers import ImageContentSerializer

class ValidateToken(APIView): # pragma: no cover
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        return Response({'Valid' : True})

class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    lookup_field = 'name'
    def get_queryset(self):
        if self.request.user.is_authenticated \
            and not self.request.user.is_superuser:
            groups = self.request.user.groups.all()
        else:
            groups = Group.objects.all()
        return groups

class ProjectViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    lookup_field = 'slug'

    def get_queryset(self):
        group = Group.objects.get(name=self.kwargs['parent_lookup_group'])
        projects = Project.objects.filter(
            group=group.id)
        return projects

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        if user.is_superuser:
            resp = Response(None, status=status.HTTP_401_UNAUTHORIZED)
        else:
            group = Group.objects.get(name=self.kwargs['parent_lookup_group'])
            if not group in user.groups.all():
                resp = Response(None, status=status.HTTP_401_UNAUTHORIZED)
            else:
                serializer.validated_data['created_by_id'] = str(user.id)
                serializer.validated_data['group_id'] = str(group.id)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                resp = Response(serializer.data,
                                status=status.HTTP_201_CREATED,
                                headers=headers)
        return resp

class SectionViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    serializer_class = SectionSerializer
    queryset = Section.objects.all()
    lookup_field = 'slug'
    def get_queryset(self):
        project = Project.objects.get(
            slug=self.kwargs['parent_lookup_project'])
        sections = Section.objects.filter(project=project)
        return sections
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = Project.objects.get(slug=kwargs['parent_lookup_project'])
        user = self.request.user
        if user.is_superuser:
            resp = Response(None, status=status.HTTP_401_UNAUTHORIZED)
        else:
            if not project.group in user.groups.all():
                resp = Response(None, status=status.HTTP_401_UNAUTHORIZED)
            else:
                serializer.validated_data['created_by_id'] = str(user.id)
                serializer.validated_data['project_id'] = str(project.id)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                resp = Response(serializer.data,
                                status=status.HTTP_201_CREATED,
                                headers=headers)
        return resp

class ImageContentViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    serializer_class = ImageContentSerializer
    queryset = ImageContent.objects.all()
    lookup_field = 'slug'

    def get_queryset(self):
        section = Section.objects.get(
            slug=self.kwargs['parent_lookup_section'])
        images = ImageContent.objects.filter(section=section)
        return images

    def create(self, request, *args, **kwargs):
        section = Section.objects.get(slug=kwargs['parent_lookup_section'])
        if section.is_gallery:
            images = ImageContent.objects.filter(
                section=section).order_by('-id')
            if images:
                request.data['name'] = str(int(images[0].name) + 1)
                request.data['slug'] = str(int(images[0].name) + 1)
            else:
                request.data['name'] = '1'
                request.data['slug'] = '1'
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        if user.is_superuser:
            resp = Response(None, status=status.HTTP_401_UNAUTHORIZED)
        else:
            if not section.project.group in user.groups.all():
                resp = Response(None, status=status.HTTP_401_UNAUTHORIZED)
            else:
                serializer.validated_data['created_by_id'] = str(user.id)
                serializer.validated_data['section_id'] = str(section.id)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                resp = Response(serializer.data,
                                status=status.HTTP_201_CREATED,
                                headers=headers)
        return resp

    def destroy(self, request, *args, **kwargs):
        image = ImageContent.objects.get(slug=kwargs['slug'])
        os.remove(image.image.path)
        return super(ImageContentViewSet, self).destroy(
            request, *args, **kwargs)
