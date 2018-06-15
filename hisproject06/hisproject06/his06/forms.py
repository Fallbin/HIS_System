from django.contrib.auth.forms import UserCreationForm
from .models import Doctor
from django import forms


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Doctor
        fields = ("username", "priority", "name", "sex", "id_num", "birth", "phone_num",
                  "address", "nation", "marriage", "num_all", "num_left", "dep", "_level")


class PatientRegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    nation = (
        ('0', "中国"),
        ('1', "美国"),
        ('2', "英国"),
        ('3', "韩国"),
        ('4', "朝鲜"),
        ('5', "日本"),
        ('６', "印度尼西亚"),
    )
    is_marriage = (
        ('0', "否"),
        ('1', "是"),
    )
    care_id = forms.CharField(error_messages={'required': "该诊疗卡号不存在"})
    name = forms.CharField(error_messages={'required': "姓名不能为空"})
    sex = forms.CharField(widget=forms.widgets.Select(choices=gender))
    id_num = forms.CharField(error_messages={'required': "身份证号不能为空"})
    birth = forms.DateTimeField()
    phone_num = forms.CharField(error_messages={'required': "联系方式不能为空"})
    address = forms.CharField(error_messages={'required': "住址不能为空"})
    nation = forms.CharField(widget=forms.widgets.Select(choices=nation, attrs={'class': "form-control"}))
    marriage = forms.CharField(widget=forms.widgets.Select(choices=is_marriage, attrs={'class': "form-control"}))
    job = forms.CharField()
    parent_name = forms.CharField()
    parent_real = forms.CharField()
    parent_phone = forms.CharField()
