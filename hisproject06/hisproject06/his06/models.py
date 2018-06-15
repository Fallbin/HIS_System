from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import datetime
import random

# Create your models here.


class Super(models.Model):
    super = (
        ('001', "大内科"),
        ('002', "大外科"),
        ('003', "妇儿科"),
        ('004', "五官科"),
        ('004', "急诊科"),
        ('005', "病案、中医"),
        ('006', "医技科"),
    )
    super_id = models.CharField(db_column='super_department_id', max_length=5,
                                choices=super, default="大内科", verbose_name="大科室ID", primary_key=True)
    super_name = models.CharField(db_column='super_department_name', max_length=255, verbose_name="大科室名称")

    class Meta:
        pass

    def __str__(self):
        return self.super_name


class Department(models.Model):
    super_id = models.ForeignKey(Super, models.DO_NOTHING, db_column='super_department_id')
    department_id = models.CharField(db_column='department_id', max_length=5, verbose_name="小科室ID", primary_key=True)
    department_name = models.CharField(db_column='department_name', max_length=255, verbose_name="小科室名称")
    department_address = models.CharField(db_column='department_address', max_length=255, verbose_name="房间号")

    class Meta:
        pass

    def __str__(self):
        return self.department_id


class Doctor(AbstractUser):
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
    level = (
        ('0', "医生"),
        ('1', "主任医师"),
        ('2', "主班护士"),
        ('3', "护士长"),
        ('4', "科副主任"),
        ('5', "科主任"),
        ('6', "住院医师"),
        ('7', "护士"),
        ('8', "主治医师"),
        ('9', "副主任医师"),
        ('10', "院长"),
        ('11', "副院长"),
    )
    name = models.CharField(db_column='doctor_name', max_length=255, verbose_name="姓名")
    sex = models.CharField(db_column='doctor_sex', max_length=32, choices=gender, default="male", verbose_name="性别")
    id_num = models.CharField(db_column='doctor_id_Num', max_length=255, verbose_name="身份证号")
    birth = models.DateTimeField(db_column='doctor_birth', max_length=6, verbose_name="生日", default=timezone.now)
    phone_num = models.CharField(db_column='doctor_phone_num', max_length=255, verbose_name="联系方式")
    address = models.CharField(db_column='doctor_address', max_length=255, verbose_name="住址")
    nation = models.CharField(db_column='doctor_nation', max_length=32, choices=nation, default="0", verbose_name="国籍")
    marriage = models.CharField(db_column='doctor_marriage', max_length=6,
                                choices=is_marriage, default="否", verbose_name="婚姻状况")
    num_all = models.IntegerField(db_column='doctor_num_all', default=100, verbose_name="总挂号人数")
    num_left = models.IntegerField(db_column='doctor_num_left', default=100, verbose_name="剩余挂号人数")
    dep = models.ForeignKey(Department, models.DO_NOTHING, db_column='dep_id',  default="00101", verbose_name="所属科室")
    priority = models.CharField(db_column="doctor_priority", default='1', max_length=6, verbose_name="权限")
    #_level = models.ForeignKey(Title, db_column='doc_level', max_length=5, choices=level, verbose_name="职称", default='10', on_delete=models.CASCADE)
    _level = models.CharField(db_column='doc_level', max_length=5, choices=level, verbose_name="职称", default='10')
    room = models.CharField(db_column='doc_room', max_length=255, verbose_name="科室房间", default="A栋403", blank=True)
    money = models.FloatField(db_column='doc_money', verbose_name="挂号费", default=5.0)

    class Meta(AbstractUser.Meta):
        db_table = 'Doctor'

    def __str__(self):
        return self.username


class Patient(models.Model):
    # 处理月份或者天数,确保月份或者天数一定是２位
    def clean_month(self):
        if(len(str(self)) < 2):
            return '0'+str(self)
        else:
            return str(self)

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
    _time = datetime.datetime.now()
    _time_random = random.randint(100000, 999999)
    _time_month = clean_month(_time.month)
    _time_day = clean_month(_time.day)
    _time_to_show = str(_time.year)+_time_month+_time_day+str(_time_random)
    care_id = models.CharField(db_column='care_id_num', max_length=255, verbose_name="诊疗卡号",
                               default=_time_to_show, primary_key=True,
                               error_messages={0: "该诊疗卡号不存在"})
    name = models.CharField(db_column='patient_name', max_length=255, verbose_name="姓名",
                            error_messages={1: "姓名不能为空"})
    sex = models.CharField(db_column='patient_sex', max_length=32, choices=gender, default="男", verbose_name="性别")
    id_num = models.CharField(db_column='patient_id_Num', max_length=255, verbose_name="身份证号",
                              error_messages={2: "身份证号不能为空"})
    birth = models.DateTimeField(db_column='patient_birth', max_length=6, verbose_name="生日")
    phone_num = models.CharField(db_column='patient_phone_num', max_length=255, verbose_name="联系方式",
                                 error_messages={3: "联系方式不能为空"})
    address = models.CharField(db_column='patient_address', max_length=255, verbose_name="住址",
                               error_messages={4: "住址不能为空"})
    nation = models.CharField(db_column='patient_nation', max_length=32, choices=nation, default="中国",
                              verbose_name="国籍")
    marriage = models.CharField(db_column='patient_marriage', max_length=6,
                                choices=is_marriage, default="否", verbose_name="婚姻状况")
    job = models.CharField(db_column='patient_job', max_length=255, verbose_name="工作", blank=True)
    parent_name = models.CharField(db_column='patient_parent_name', max_length=255, verbose_name="监护人", blank=True)
    parent_real = models.CharField(db_column='patient_parent_real', max_length=255, verbose_name="关系", blank=True)
    parent_phone = models.CharField(db_column='patient_parent_phone', max_length=255, verbose_name="监护人联系方式", blank=True)
    allergy = models.CharField(db_column="patient_allergy", max_length=255, verbose_name="过敏药物", blank=True)
    sick_his = models.CharField(db_column="patient_sickhis", max_length=255, verbose_name="既往病史", blank=True)
    is_deal = models.BooleanField(db_column="is_deal", verbose_name="是否处理", default=0)

    class Meta:
        pass

    def __str__(self):
        return self.care_id


# 建立职称表
class Title(models.Model):
    id = models.CharField(db_column="id", max_length=255, primary_key=True)
    name = models.CharField(db_column="name", max_length=255, verbose_name="职称")

    def __str__(self):
        return self.name


# 新建一个挂号表
class PatientSign(models.Model):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    water_id = models.IntegerField(db_column="water_id", primary_key=True)
    # care_id = models.ForeignKey(Patient, db_column="care_id", max_length=255, verbose_name="诊疗卡号", on_delete=models.CASCADE)
    care_id = models.CharField(db_column="care_id", max_length=255, verbose_name="诊疗卡号")
    patient_name = models.CharField(db_column="patient_name", max_length=255, verbose_name="病人姓名")
    patientSex = models.CharField(db_column="patient_sex", max_length=255, verbose_name="病人性别", choices=gender)
    patient_id = models.CharField(db_column="patient_id", max_length=255, verbose_name="身份证号")
    # patient_birth = models.DateTimeField(db_column="patient_birth", verbose_name="出生日期")
    patient_phone = models.CharField(db_column="patient_phone", max_length=255, verbose_name="联系方式")
    sign_time = models.DateTimeField(db_column="sign_time", verbose_name="挂号日期", default=datetime.datetime.now)
    patient_address = models.CharField(db_column="patient_address", max_length=255, verbose_name="家庭住址")
    super = models.CharField(db_column="super", max_length=255, verbose_name="科室类型")
    dep = models.CharField(db_column="dep", max_length=255, verbose_name="挂号科室")
    #doc_level = models.ForeignKey(Title, db_column="doc_level", max_length=255, verbose_name="医生职称", on_delete=models.CASCADE)
    doc_level = models.CharField(db_column="doc_level", max_length=255, verbose_name="医生职称")
    doc_name = models.CharField(db_column="doc_name", max_length=255, verbose_name="医生姓名")
    doc_room = models.CharField(db_column="doc_room", max_length=255, verbose_name="就诊房间")
    doc_sex = models.CharField(db_column="doc_sex", max_length=255, verbose_name="医生性别")
    sign_kind = models.CharField(db_column="sign_kind", max_length=255, verbose_name="挂号号别")
    is_book = models.CharField(db_column="is_book", max_length=5, verbose_name="是否购买病历")
    should_pay = models.FloatField(db_column="should_pay", verbose_name="应缴金额")
    real_pay = models.FloatField(db_column="real_pay", verbose_name="实付金额")
    ret_pay = models.FloatField(db_column="ret_pay", verbose_name="找回金额")
    care_num = models.IntegerField(db_column='care_num', verbose_name="诊疗号", default=1)
    is_deal = models.BooleanField(db_column="is_deal", verbose_name="是否处理", default=0)

    def __str__(self):
        return self.water_id


# 新建一个表做流水号的记录
class WaterNum(models.Model):
    id = models.IntegerField(db_column="water_num", primary_key=True)

    def __str__(self):
        return self.id


class WorkTime(models.Model):
    Time = (
        ('0', "早上"),
        ('1', "中午"),
        ('2', "晚上"),
        ('3', "全天"),
    )
    id = models.IntegerField(db_column="id", primary_key=True, default=1)
    work_date = models.DateField(db_column="date", verbose_name="值班日期")
    time = models.CharField(max_length=255, verbose_name="值班时间", choices=Time)
    doc_id = models.CharField(max_length=255, verbose_name="医生工号")
    dep = models.CharField(max_length=255, verbose_name="所属科室")

    def __str__(self):
        return self.doc_id


class MedicineType(models.Model):
    Type=(
        ('0', "消化系统药物"),
        ('1', "镇热镇痛类药品"),
    )
    me_id = models.CharField(max_length=255, primary_key=True)
    me_name = models.CharField(max_length=255, verbose_name="药品大类")

    def __str__(self):
        return self.me_name


class MedicineKind(models.Model):
    me_id = models.ForeignKey(MedicineType, models.DO_NOTHING, db_column='me_id')
    sm_id = models.CharField(db_column='sm_id', max_length=5, verbose_name="药品种类ID", primary_key=True)
    sm_name = models.CharField(db_column='sm_name', max_length=255, verbose_name="药品种类名称")

    def __str__(self):
        return self.sm_id


class Medicine(models.Model):
    sm_id = models.ForeignKey(MedicineKind, models.DO_NOTHING, db_column='sm_id')
    medicineName = models.CharField(max_length=255, db_column="medicineName", verbose_name="药品名称")
    medicineId = models.CharField(max_length=255, db_column="medicineId", verbose_name="药品ID")
    max_num = models.IntegerField(db_column="max_num", verbose_name="药品使用最大量")
    all_num = models.IntegerField(db_column="all_num", verbose_name="药品总量")
    left_num = models.IntegerField(db_column="left_num", verbose_name="药品剩余量")
    price = models.IntegerField(db_column="price", verbose_name="单价", default=100)

    def __str__(self):
        return self.medicineId


class Check_Pro(models.Model):
    pro_id = models.CharField(max_length=255, db_column="pro_id", verbose_name="项目ID")
    pro_name = models.CharField(max_length=255, db_column="pro_name", verbose_name="项目名称")
    price = models.IntegerField(db_column="price", verbose_name="价格")

    def __str__(self):
        return self.pro_id


class Sick_his(models.Model):
    sick_id = models.IntegerField(max_length=255, db_column="id", primary_key=True)    # 流水号做唯一ID,可以和挂号信息勾连
    # care_id = models.ForeignKey(Patient, max_length=255, db_column="care_id", verbose_name="诊疗卡号", on_delete=models.CASCADE)
    care_id = models.CharField(max_length=255, db_column="care_id", verbose_name="诊疗卡号")
    sick_symtop = models.CharField(max_length=255, db_column="sick_symtop", verbose_name="症状描述")
    result = models.CharField(max_length=255, db_column="result", verbose_name="诊断结果")
    medi_use = models.CharField(max_length=255, db_column="medi_use", verbose_name="处方")
    sick_pro = models.CharField(max_length=255, db_column="sick_pro", verbose_name="检查项目")

    def __str__(self):
        return self.sick_id



