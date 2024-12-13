# 標準庫 (Standarddd library)
import json

# Django 相關 (Django imports)
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

# DRF 相關 (Django REST framework imports)
from rest_framework import generics, status, viewsets,permissions
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
# 應用內的自定義模組 (Local app imports)
from .models import CustomUser, Course
from .serializers import (
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    CustomUserSerializer,
    CourseSerializer,
)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


#測試登入
@login_required
def check_auth_status(request):
    return JsonResponse({
        'isAuthenticated': True,
        'username': request.user.username,
    })

# 前端註冊資料驗證
@api_view(['POST'])
def register_user(request):
    permission_classes = [AllowAny]
    if request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from .serializers import LoginSerializer

@ensure_csrf_cookie
def get_csrf_token(request):
    """
    返回 CSRF Token 的视图
    """
    csrf_token = get_token(request)  # 生成或获取当前请求的 CSRF Token
    return JsonResponse({'csrfToken': csrf_token})

def login_view(request):
    if request.method == 'POST':
        try:

            data = json.loads(request.body)  # 從請求體中解析 JSON 數據

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)
        print(data)
        # 使用 LoginSerializer 進行資料驗證
        serializer = LoginSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return JsonResponse({'success': True, 'message': 'Logged in'})
        else:
            # 返回驗證錯誤訊息
            return JsonResponse({'success': False, 'message': serializer.errors}, status=401)

    return JsonResponse({'error': 'Invalid method'}, status=400)

class PasswordResetRequestView(generics.GenericAPIView):
    """
    密碼重設請求 API 端點
    """
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = CustomUser.objects.get(email=email)

        # 生成重設密碼的 token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # 構建重設密碼的連結
        reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"

        # 渲染郵件模板
        message = render_to_string('password_reset_email.html', {
            'user': user,
            'reset_url': reset_url,
        })

        # 發送郵件
        email_message = EmailMessage(
            subject='重設您的密碼',
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )
        email_message.send(fail_silently=False)

        return Response({'message': '重設密碼的郵件已發送。'}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(generics.GenericAPIView):
    """
    密碼重設確認 API 端點
    """
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [AllowAny]

    def post(self, request, uid, token, *args, **kwargs):
        data = request.data.copy()
        data['uid'] = uid
        data['token'] = token
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': '密碼已成功重設。'}, status=status.HTTP_200_OK)


from .models import StudentCourse
from .serializers import StudentCourseSerializer


class StudentCourseViewSet(viewsets.ModelViewSet):
    serializer_class = StudentCourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return StudentCourse.objects.filter(student=self.request.user)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

