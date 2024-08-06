from django.contrib import admin


from lms.models import (Category,Course)

# Register your models here.

admin.site.register(Category)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    list_display = [
        'title', 
        'slug', 
        'instructor', 
        'category',
        'created_at', 
        'status'
        ]
    
    list_filter = [
        'status',
        'instructor',
        'category', 
        'created_at', 
        'published_at'
        ]
    
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['instructor']
    date_hierarchy = 'created_at'
    ordering = ['status', 'created_at']