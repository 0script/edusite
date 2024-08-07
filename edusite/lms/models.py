from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

# Create your models here.

class Category(models.Model):
    # Category: This model categorizes courses (e.g., "Programming", "Design").
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Course.Status.PUBLISHED)


class Course(models.Model):
    # Course: This represents a course with fields for the title, description, instructor, category, price, and timestamps.
    
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=255)
    slug=models.SlugField(verbose_name=("Slug"),max_length=250,unique_for_date='published_at')
    status=models.CharField(verbose_name=("Status"),default=Status.DRAFT,max_length=2)
    description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
    published_at=models.DateField(blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = models.Manager()
    published = PublishedManager()
    
    def save(self,*args, **kwargs):
        if self.published_at is None and self.status == self.Status.PUBLISHED:
            self.published_at=timezone.now()
        super().save(*args, **kwargs)

    def get_categories(self):
        courses=Course.published.all()
        categories=[]
        for course in courses:
            if course.category.name in categories:
                continue
            else:
                categories.append(course.category.name)
        categories=[ {'name':categories[x],'id':x+1} for x in range(len(categories)) ]
        return categories

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return self.title

# class CourseProgression(models.Model):
#     course=models.ForeignKey(Course, verbose_name=_(""), on_delete=models.CASCADE)