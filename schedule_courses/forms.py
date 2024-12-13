from django import forms


class XLSUploadForm(forms.Form):
    xls_file = forms.FileField(label="上傳 XLS 檔案")  # 文件字段（支持 XLS）
