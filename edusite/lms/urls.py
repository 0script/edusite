from django.urls import path

from . import views

app_name='lms'

urlpatterns = [
    path('',views.index,name='index'),
    path('<int:id>/',views.course_detail,name='course_detail'),
]

