from django.contrib.auth.models import AbstractUser
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from taggit.managers import TaggableManager

from MyGitHub import settings


class Category(MPTTModel):
    name = models.CharField(max_length=50)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='categories')

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField()
    tags = TaggableManager()
    category = models.ForeignKey('Category', on_delete=models.DO_NOTHING, related_name='projects', related_query_name='project')

    @classmethod
    def search(cls, project_name, user):
        projects = []
        try:
            project = cls.objects.get(name=project_name, category__owner_id=user.id)
            projects.append(project)
        except cls.DoesNotExist:
            pass
        words = project_name.split()
        projects.extend(cls.objects.filter(tags__name__in=words, category__owner_id=user.id).distinct())
        for name in words:
            if len(name) >= 3:
                try:
                    project = cls.objects.get(name=name, category__owner_id=user.id)
                    projects.append(project)
                except cls.DoesNotExist:
                    pass
        seen = set()
        seen_add = seen.add
        return [x for x in projects if not (x in seen or seen_add(x))]


class MyUser(AbstractUser):
    token = models.CharField(max_length=40, help_text='Enter Github.com personal access token.')
