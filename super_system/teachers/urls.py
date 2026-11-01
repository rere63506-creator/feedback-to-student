from django.urls import path
from teachers import views

urlpatterns=[
    path('',views.welcome,name='welcome'),
    path('teacher/register/',views.teacher_register,name='teacher_register'),
    path('teacher/login/',views.teacher_login,name='teacher_login'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('student/login/',views.student_login,name='student_login'),
    path('student/detail/<int:student_id>/',views.student_detail,name='student_detail'),
    path('edit/student/<int:student_id>/',views.edit_student,name='edit_student'),
    path('delete/student/<int:student_id>/',views.delete_student,name='delete_student')
]