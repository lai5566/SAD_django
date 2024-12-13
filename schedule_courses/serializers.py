
from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from .models import Course
CustomUser = get_user_model()

class CourseSerializer(serializers.ModelSerializer):
    """
    序列化 Course 模型的所有字段。
    """
    class Meta:
        model = Course
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    """
    用於用戶註冊的序列化器，處理用戶資料的驗證和創建。
    """
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        覆寫 create 方法，使用自訂的 create_user 方法來創建用戶，確保密碼被正確加密。
        """
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']

        )
        return user

    def create_superuser(self, email, username, password=None):
        """
        創建超級用戶，設置必需的 is_admin 和 is_superuser 屬性。
        """
        user = self.create_user(
            email=email,
            username=username,
            password=password
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class LoginSerializer(serializers.Serializer):
    """
    用於用戶登入的序列化器，處理電子郵件和密碼的驗證。
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        驗證用戶的電子郵件和密碼是否正確。
        """
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request=self.context.get('request'), email=email, password=password)
        if not user:
            raise serializers.ValidationError('Unable to log in with provided credentials.')
        data['user'] = user
        return data


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    用於處理密碼重設請求的序列化器，驗證電子郵件是否存在。
    """
    email = serializers.EmailField()

    def validate_email(self, value):
        """
        檢查提交的電子郵件是否存在於用戶資料庫中。
        """
        try:
            user = CustomUser.objects.get(email=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("沒有找到與此郵件地址相關的帳戶。")
        return value
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password1 = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        try:
            uid = attrs.get('uid')
            token = attrs.get('token')
            new_password1 = attrs.get('new_password1')
            new_password2 = attrs.get('new_password2')

            if new_password1 != new_password2:
                raise serializers.ValidationError("新密碼和確認密碼不匹配。")

            uid = urlsafe_base64_decode(uid).decode()
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            raise serializers.ValidationError("無效的重設密碼連結。")

        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError("無效或已過期的重設密碼連結。")

        attrs['user'] = user
        return attrs

    def save(self, **kwargs):
        user = self.validated_data['user']
        new_password = self.validated_data['new_password1']
        user.set_password(new_password)
        user.save()
        return user

# 選課
from .models import StudentCourse
#
class StudentCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCourse
        fields = ['id', 'student', 'course', 'selected_at']
        read_only_fields = ['student', 'selected_at']


