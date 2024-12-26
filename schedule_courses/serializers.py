
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


from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    # 原本就需要的欄位
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    # 新增想要回傳的欄位，並標記為只讀（read_only=True）
    id = serializers.IntegerField(read_only=True)
    is_admin = serializers.BooleanField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)

    def validate(self, data):
        # 取得前端傳入的 email、password
        email = data.get('email')
        password = data.get('password')

        # 用 authenticate 驗證帳密
        user = authenticate(
            request=self.context.get('request'),
            username=email,  # 注意: 若你的自定義 User Model 用的是 email 做 username field，要這樣寫
            password=password
        )
        if not user:
            raise serializers.ValidationError('無法使用提供的憑證登入。')

        #驗證成功：把想要回傳的欄位資訊，塞到 validated_data
        # === 這裡加上 print 來確認流程有走到 ===
        print("i here")
        print(f"user.id: {user.id}")
        print(f"user.is_admin: {user.is_admin}")
        print(f"user.is_superuser: {user.is_superuser}")

        data['id'] = user.id
        data['is_admin'] = user.is_admin
        data['is_superuser'] = user.is_superuser
        # 也可視需求加入更多自訂資訊

        # 保持對應 user instance 的參考，後續可能有需要
        data['user'] = user
        print('sdef')
        print(data)
        return data
# 選課
from .models import StudentCourse
#
class StudentCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCourse
        fields = ['id', 'student', 'course', 'selected_at']
        read_only_fields = ['student', 'selected_at']


#重設密碼
# serializers.py


from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()

# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)
#
#     def validate(self, data):
#         email = data.get('email')
#         password = data.get('password')
#
#         if email and password:
#             user = authenticate(request=self.context.get('request'), username=email, password=password)
#             if not user:
#                 raise serializers.ValidationError('無法使用提供的憑證登入。')
#         else:
#             raise serializers.ValidationError('必須包含 "email" 和 "password"。')
#
#         data['user'] = user
#         return data

# your_app_name/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

# your_app_name/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

User = get_user_model()

class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        try:
            uid = attrs.get('uid')
            token = attrs.get('token')
            password = attrs.get('new_password')

            uid = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=uid)

            token_generator = PasswordResetTokenGenerator()
            if not token_generator.check_token(user, token):
                raise serializers.ValidationError({'token': '無效的重設令牌。'})

            attrs['user'] = user
            return attrs
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError('無效的重設令牌。')
