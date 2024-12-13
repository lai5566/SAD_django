# Register your models here.
from .models import CustomUser,Course,StudentCourse
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
import xlrd
# # Register your models here.
# admin.site.register(CustomUser)
#
from django import forms
from django.shortcuts import render
from django.urls import path
from django.http import HttpResponseRedirect
from .forms import XLSUploadForm
import pandas as pd

class CustomUserAdmin(UserAdmin):
    # 可以根据需要自定义下面的属性
    model = CustomUser
    list_display = ('email', 'username', 'is_admin', 'is_superuser')
    list_filter = ('is_admin', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_admin', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_admin', 'is_superuser'),
        }),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)


# 替换之前的 admin.site.register(CustomUser)
admin.site.register(CustomUser, CustomUserAdmin)

# # 自定义 CSV 上传表单
# class CSVUploadForm(forms.Form):
#     csv_file = forms.FileField()
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    change_list_template = "admin/course_changelist.html"  # 重定義模板

    def get_urls(self):
        urls = super().get_urls()  # 獲取默認的管理 URL
        custom_urls = [
            path('upload-xls/', self.upload_xls, name='upload_xls'),  # 增加上傳 XLS 的路徑
        ]
        return custom_urls + urls  # 新增路徑至管理系統

    def upload_xls(self, request):
        if request.method == "POST":  # 如果是 POST 請求
            form = XLSUploadForm(request.POST, request.FILES)
            if form.is_valid():
                xls_file = form.cleaned_data["xls_file"]  # 提取文件對象
                try:
                    # 將上傳的 .xls 文件轉為 DataFrame，跳過前 4 行
                    df = pd.read_excel(xls_file, skiprows=4, engine='xlrd')

                    # 確保 DataFrame 移除第 5 列 (索引為 4 的列)
                    df = df.drop(df.columns[4], axis=1)

                    # 遍歷每一行，將數據寫入資料庫
                    for _, row in df.iterrows():
                        Course.objects.create(
                            semester=str(row[0]),
                            primary_instructor=row[1],
                            course_code_new=row[2],
                            department_code=str(row[3]),
                            core_code=str(row[4]),
                            course_group=str(row[5]),
                            grade=str(row[6]),
                            class_group=row[7],
                            course_name_cn=row[8],
                            course_name_en=row[9],
                            instructor_name=row[10],
                            enrollment=int(row[11]),
                            male_students=int(row[12]),
                            female_students=int(row[13]),
                            credits=int(row[14]),
                            weeks=row[15],
                            hours_per_week=float(row[16]),
                            course_type_code=str(row[17]),
                            course_type=row[18],
                            location=row[19],
                            weekday=str(row[20]),
                            class_period=row[21],
                            notes=row[22] if len(row) > 22 else None,
                            course_summary_cn=row[23] if len(row) > 23 else None,
                            course_summary_en=row[24] if len(row) > 24 else None,
                            primary_instructor_code_old=str(row[25]),
                            course_code_old=row[26],
                            schedule_code_old=row[27],
                            schedule_name_old=row[28],
                            instructor_code_old=row[29],
                        )
                except Exception as e:
                    self.message_user(request, f"Error processing XLS file: {e}", level="error")
                else:
                    self.message_user(request, "XLS file successfully uploaded")
                return HttpResponseRedirect("../")  # 上傳完成後重定向至管理界面

        form = XLSUploadForm()
        context = {
            **self.admin_site.each_context(request),  # 包含admin上的上下文
            'form': form
        }
        return render(request, "admin/xls_upload_form.html", context)
admin.site.register(StudentCourse)