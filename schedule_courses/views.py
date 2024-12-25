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

# def login_view(request):
#     if request.method == 'POST':
#         try:
#
#             data = json.loads(request.body)  # 從請求體中解析 JSON 數據
#
#         except json.JSONDecodeError:
#             return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)
#         print(data)
#         # 使用 LoginSerializer 進行資料驗證
#         serializer = LoginSerializer(data=data, context={'request': request})
#         if serializer.is_valid():
#             user = serializer.validated_data['user']
#             login(request, user)
#             return JsonResponse({'success': True, 'message': 'Logged in'})
#         else:
#             # 返回驗證錯誤訊息
#             return JsonResponse({'success': False, 'message': serializer.errors}, status=401)
#
#     return JsonResponse({'error': 'Invalid method'}, status=400)
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)

        serializer = LoginSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)

            user_data = serializer.to_representation(serializer.validated_data)

            return JsonResponse({
                'success': True,
                'message': 'Logged in successfully.',
                'user': user_data,
            })
        else:
            return JsonResponse({'success': False, 'message': serializer.errors}, status=401)

    return JsonResponse({'error': 'Invalid method'}, status=400)


from .models import StudentCourse
from .serializers import StudentCourseSerializer


class StudentCourseViewSet(viewsets.ModelViewSet):
    serializer_class = StudentCourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return StudentCourse.objects.filter(student=self.request.user)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

# 密碼重設
# views.py

# your_app_name/views.py

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PasswordResetRequestSerializer, PasswordResetConfirmSerializer
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

@method_decorator(csrf_exempt, name='dispatch')
class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]  # 確保允許任何人訪問

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # 為了安全性，不顯示用戶是否存在
                return Response(
                    {'message': '密碼重設郵件已發送。'},
                    status=status.HTTP_200_OK
                )

            # 生成重設令牌和 uid
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # 構建重設連結
            reset_link = f"{settings.FRONTEND_URL}/reset-password/?uid={uid}&token={token}"

            # 發送郵件
            subject = '密碼重設請求'
            message = f'''
您收到這封郵件是因為我們收到您帳戶的密碼重設請求。

請點擊以下連結來重設您的密碼：
{reset_link}

如果您沒有發起此請求，請忽略此郵件。

謝謝！
            '''
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                return Response(
                    {'message': '密碼重設郵件已發送。'},
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                logger.error(f'Error sending password reset email: {e}')
                return Response(
                    {'error': '無法發送郵件，請稍後再試。'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            logger.error(f'Password reset request invalid: {serializer.errors}')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]  # 確保允許任何人訪問

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            new_password = serializer.validated_data['new_password']
            user.set_password(new_password)
            user.save()
            return Response(
                {'message': '密碼已成功重設。'},
                status=status.HTTP_200_OK
            )
        else:
            logger.error(f'Password reset confirm invalid: {serializer.errors}')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class PasswordResetConfirmView(APIView):
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            new_password = serializer.validated_data['new_password']
            user.set_password(new_password)
            user.save()
            return Response(
                {'message': '密碼已成功重設。'},
                status=status.HTTP_200_OK
            )
        else:
            logger.error(f'Password reset confirm invalid: {serializer.errors}')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#改密碼
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth.hashers import check_password
class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')

        if not current_password or not new_password:
            return Response({'detail': '缺少必要參數'}, status=status.HTTP_400_BAD_REQUEST)

        # 驗證目前密碼是否正確
        if not check_password(current_password, user.password):
            return Response({'detail': '當前密碼不正確'}, status=status.HTTP_400_BAD_REQUEST)

        # 更新密碼
        user.set_password(new_password)
        user.save()
        return Response({'detail': '密碼更新成功'}, status=status.HTTP_200_OK)



#登出
# views.py
from django.contrib.auth import logout
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["POST"])
def logout_view(request):
    logout(request)  # 會自動清除 request.session
    return Response({"detail": "已登出"}, status=200)