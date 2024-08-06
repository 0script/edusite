from django.shortcuts import render,get_object_or_404
from django.http import Http404

from lms.models import Course

# Create your views here.

def index(request):
    courses=Course.published.all()
    categories=Course().get_categories()

    context={
        'courses':courses,
        'categories':categories,
    }
    return render(request,template_name='lms/index.html',context=context)

def course_detail(request,id):
    course=get_object_or_404(Course,id=id,status=Course.Status.PUBLISHED)
    return render(request,'lms/course/course_detail.html',{'course':course})