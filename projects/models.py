from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from taggit.managers import TaggableManager


class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True, on_delete=models.CASCADE)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=50, unique=True)
    url = models.URLField()
    tags = TaggableManager()
    category = models.ForeignKey('Category', on_delete=models.DO_NOTHING, related_name='projects', related_query_name='project')

    @classmethod
    def search(cls, project_name):
        projects = []
        try:
            project = cls.objects.get(name=project_name)
            projects.append(project)
        except cls.DoesNotExist:
            pass
        words = project_name.split()
        projects.extend(cls.objects.filter(tags__name__in=words).distinct())
        for name in words:
            if len(name) >= 3:
                try:
                    project = cls.objects.get(name=name)
                    projects.append(project)
                except cls.DoesNotExist:
                    pass
        seen = set()
        seen_add = seen.add
        return [x for x in projects if not (x in seen or seen_add(x))]
