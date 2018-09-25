import shutil

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from rest_framework.test import APIClient

from content.models import Project
from content.models import Section
from content.models import ImageContent

class ModelTestCase(TestCase):

    def setUp(self):
        group = Group(name='emptygroup')
        group.save()
        group = Group(name='testgroup')
        group.save()
        user = User(email='empty@test.com', username='empty@test.com')
        user.set_password('password')
        user.save()
        emptygroup = Group.objects.get(name='emptygroup')
        user.groups.add(emptygroup)
        user.save()
        user = User(email='test@test.com', username='test@test.com')
        user.set_password('password')
        user.save()
        user.groups.add(group)
        user.save()
        superuser = User(email="super@test.com",
                         username='super@test.com',
                         is_superuser=True)
        superuser.set_password('password')
        superuser.save()
        project = Project(
            name='project', slug='project', created_by=user, group=group)
        project.save()
        section = Section(project=project, name='section', slug='section',
                          is_gallery=False, created_by=user)
        section.save()
        image_content = ImageContent(name='image_content',
                                     slug='imagecontent',
                                     created_by=user, section=section)
        image_content.image = SimpleUploadedFile(
            name='test.jpeg',
            content=open(settings.BASE_DIR +
                         '/content/tests/test.jpeg', 'rb').read(),
            content_type='image/jpeg')
        image_content.save()
        db_image_content = ImageContent.objects.get(slug='imagecontent')
        self.assertEqual(str(db_image_content), image_content.name)
        shutil.rmtree(settings.MEDIA_ROOT + '/' + user.groups.first().name)


    def test_model(self):
        user = User.objects.get(email='test@test.com')
        project = Project(
            name='project2', slug='project2', created_by=user,
            group=user.groups.first())
        project.save()
        db_project = Project.objects.get(slug='project2')
        self.assertEqual(str(db_project), project.name)
        section = Section(project=project, name='section2', slug='section2',
                          is_gallery=False, created_by=user)
        section.save()
        db_section = Section.objects.get(slug='section2')
        self.assertEqual(str(db_section), project.name + ':' + section.name)
        image_content = ImageContent(name='image_content2',
                                     slug='imagecontent2',
                                     created_by=user, section=section)
        image_content.image = SimpleUploadedFile(
            name='test.jpeg',
            content=open(settings.BASE_DIR +
                         '/content/tests/test.jpeg', 'rb').read(),
            content_type='image/jpeg')
        image_content.save()
        db_image_content = ImageContent.objects.get(slug='imagecontent2')
        self.assertEqual(str(db_image_content), image_content.name)
        shutil.rmtree(settings.MEDIA_ROOT + '/' + user.groups.first().name)

    def test_get(self):
        client = APIClient()

        # Regular user
        client.login(username='test@test.com', password='password')
        response = client.get('http://localhost:8000/groups/')
        self.assertEqual(response.status_code, 200)
        response = client.get(
            'http://localhost:8000/groups/testgroup/projects/')
        self.assertEqual(response.status_code, 200)
        response = client.get(
            'http://localhost:8000/groups/testgroup/' +
            'projects/project/sections/')
        self.assertEqual(response.status_code, 200)
        response = client.get(
            'http://localhost:8000/groups/testgroup/' +
            'projects/project/sections/section/images/')
        self.assertEqual(response.status_code, 200)
        response = client.get(
            'http://localhost:8000/groups/testgroup/' +
            'projects/project/sections/section/images/imagecontent/')
        self.assertEqual(response.status_code, 200)

        # Super user
        client.login(username='super@test.com', password='password')
        response = client.get('http://localhost:8000/groups/')
        self.assertEqual(response.status_code, 200)
        response = client.get(
            'http://localhost:8000/groups/testgroup/projects/')
        self.assertEqual(response.status_code, 200)
        response = client.get(
            'http://localhost:8000/groups/testgroup/' +
            'projects/project/sections/')
        self.assertEqual(response.status_code, 200)
        response = client.get(
            'http://localhost:8000/groups/testgroup/' +
            'projects/project/sections/section/images/')
        self.assertEqual(response.status_code, 200)
        response = client.get(
            'http://localhost:8000/groups/testgroup/' +
            'projects/project/sections/section/images/imagecontent/')
        self.assertEqual(response.status_code, 200)

    def test_post_regular_user(self):
        client = APIClient()

        # User not in group
        client.login(username='empty@test.com', password='password')
        data = {
            'name': 'test3',
            'slug': 'test3',
            'description' : 'test3 description'
        }
        response = client.post(
            'http://localhost:8000/groups/testgroup/projects/',
            data)
        self.assertEqual(response.status_code, 401)

        data = {
            'name': 'testsection3',
            'slug': 'testsection3',
            'is_gallery' : False
        }
        response = client.post(
            'http://localhost:8000/groups/testgroup/projects/project/sections/',
            data)
        self.assertEqual(response.status_code, 401)

        image = SimpleUploadedFile(
            name='test.jpeg',
            content=open(settings.BASE_DIR +
                         '/content/tests/test.jpeg', 'rb').read(),
            content_type='image/jpeg')
        data = {
            'name': 'test3',
            'slug': 'test3',
            'image' : image
        }
        response = \
        client.post(
            'http://localhost:8000/groups/testgroup/projects/project/' +
            'sections/section/images/', data)
        self.assertEqual(response.status_code, 401)

        # User in group
        client.login(username='test@test.com', password='password')
        data = {
            'name': 'test3',
            'slug': 'test3',
            'description' : 'test3 description'
        }
        response = client.post(
            'http://localhost:8000/groups/testgroup/projects/',
            data)
        self.assertEqual(response.status_code, 201)
        # Non gallery
        data = {
            'name': 'testsection3',
            'slug': 'testsection3',
            'is_gallery' : False
        }
        response = client.post(
            'http://localhost:8000/groups/testgroup/projects/test3/sections/',
            data)
        self.assertEqual(response.status_code, 201)
        image = SimpleUploadedFile(
            name='test.jpeg',
            content=open(settings.BASE_DIR +
                         '/content/tests/test.jpeg', 'rb').read(),
            content_type='image/jpeg')
        data = {
            'name' : 'testimage3',
            'slug' : 'testimage3',
            'image' : image
        }
        response = \
        client.post(
            'http://localhost:8000/groups/testgroup/projects/test3/sections/' +
            'testsection3/images/', data)
        self.assertEqual(response.status_code, 201)

        # Gallery 
        data = {
            'name': 'test3',
            'slug': 'test3',
            'is_gallery' : True
        }
        response = client.post(
            'http://localhost:8000/groups/testgroup/projects/test3/sections/',
            data)
        self.assertEqual(response.status_code, 201)
        image = SimpleUploadedFile(
            name='test.jpeg',
            content=open(settings.BASE_DIR +
                         '/content/tests/test.jpeg', 'rb').read(),
            content_type='image/jpeg')
        data = {
            'image' : image
        }
        response = \
        client.post(
            'http://localhost:8000/groups/testgroup/projects/test3/sections/' +
            'test3/images/', data)
        self.assertEqual(response.status_code, 201)
        image = SimpleUploadedFile(
            name='testupdate.png',
            content=open(settings.BASE_DIR +
                         '/content/tests/testupdate.png', 'rb').read(),
            content_type='image/png')
        data = {
            'image' : image
        }
        response = \
        client.post(
            'http://localhost:8000/groups/testgroup/projects/test3/sections/' +
            'test3/images/', data)
        self.assertEqual(response.status_code, 201)
        image_content = ImageContent.objects.get(slug='1')
        image = SimpleUploadedFile(
            name='testupdate.png',
            content=open(settings.BASE_DIR +
                         '/content/tests/testupdate.png', 'rb').read(),
            content_type='image/png')
        data = {
            'id': image_content.id,
            'section': image_content.section_id,
            'name': '1',
            'slug': '1',
            'image' : image,
            'created_by': image_content.created_by_id
        }
        response = \
        client.put(
            'http://localhost:8000/groups/testgroup/projects/test3/sections/' +
            'test3/images/1/', data)
        self.assertEqual(response.status_code, 200)
        response = \
        client.delete(
            'http://localhost:8000/groups/testgroup/projects/test3/sections/' +
            'test3/images/1/', data)
        self.assertEqual(response.status_code, 204)

    def test_post_super_user(self):
        client = APIClient()
        client.login(username='super@test.com', password='password')
        data = {
            'name': 'test3',
            'slug': 'test3',
            'description' : 'test3 description'
        }
        response = client.post(
            'http://localhost:8000/groups/testgroup/projects/',
            data)
        self.assertEqual(response.status_code, 401)
        data = {
            'name': 'test3',
            'slug': 'test3',
            'is_gallery' : False
        }
        response = client.post(
            'http://localhost:8000/groups/testgroup/projects/project/sections/',
            data)
        self.assertEqual(response.status_code, 401)
        image = SimpleUploadedFile(
            name='test.jpeg',
            content=open(settings.BASE_DIR +
                         '/content/tests/test.jpeg', 'rb').read(),
            content_type='image/jpeg')
        data = {
            'name': 'testimage3',
            'slug': 'testimage3',
            'image' : image
        }
        response = client.post(
            'http://localhost:8000/groups/testgroup/projects/test3/sections/' +
            'section/images/', data)
        self.assertEqual(response.status_code, 401)
