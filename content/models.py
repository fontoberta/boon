from django.db import models
from django.contrib.auth.models import User, Group

class BaseModel(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=25)
    def __str__(self):
        return u'%s' % self.name
    class Meta:
        abstract = True

class Project(BaseModel):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    description = models.TextField()
    class Meta:
        unique_together = ('slug', 'group',)

class Section(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    is_gallery = models.BooleanField()
    def __str__(self):
        return u"%s:%s" % (self.project.name, self.name)
    class Meta:
        unique_together = ('slug', 'project',)

def get_upload_to(instance, filename):
    return '%s/%s/%s/%s' % (
        instance.created_by.groups.first().name,
        instance.section.project.slug, instance.section.slug, filename)

class ImageContent(BaseModel):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_upload_to)
    class Meta:
        unique_together = ('slug', 'section',)
