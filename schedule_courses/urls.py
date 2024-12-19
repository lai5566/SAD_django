# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import CourseViewSet
# from . import views
# from django.urls import path
# from .views import  login_view,get_csrf_token,PasswordResetRequestView
# from .views import check_auth_status
# router = DefaultRouter()
# router.register(r'courses', views.CourseViewSet)
#
# app_name = "schedule_courses"
# urlpatterns = [
#     path('api/', include(router.urls)),
#     # ('api-auth/', include('rest_framework.urls')),
#     path('api/signup/', views.register_user, name='register_user'),
#     # path('api/userslogin/', login_user, name='login_user'),
#     # path('api/auth/status/', check_auth_status, name='check_auth_status'),
#     path('api/auth/login/', login_view, name='login'),
#     path('csrf/', get_csrf_token, name='get_csrf_token'),  # 定义 CSRF 接口
#
#     path('api/password_reset/', PasswordResetRequestView.as_view(), name='password_reset'),
# ]
# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, StudentCourseViewSet, login_view, get_csrf_token, PasswordResetRequestView, \
    check_auth_status, register_user,PasswordResetConfirmView

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'student-courses', StudentCourseViewSet, basename='student-courses')  # 新增選課路由

app_name = "schedule_courses"
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/signup/', register_user, name='register_user'),
    path('api/auth/login/', login_view, name='login'),
    path('csrf/', get_csrf_token, name='get_csrf_token'),
    path('api/auth/status/', check_auth_status, name='check_auth_status'),
    path('api/password_reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('api/password_reset_confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
