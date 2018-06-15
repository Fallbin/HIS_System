from django.shortcuts import render, HttpResponse, get_object_or_404
from .forms import RegisterForm, PatientRegisterForm
from django.contrib.auth.decorators import login_required
from his06 import models
from django.core import serializers
from django.utils import timezone
from django.utils.timezone import timedelta


def register(request):
    # 只有当请求为 POST 时，才表示用户提交了注册信息
    if request.method == 'POST':
        # request.POST 是一个类字典数据结构，记录了用户提交的注册信息
        # 这里提交的就是用户名（username）、密码（password）、权限（priority）...
        # 用这些数据实例化一个用户注册表单
        form = RegisterForm(request.POST)

        # 验证数据的合法性
        if form.is_valid():
            # 如果提交数据合法，调用表单的 save 方法将用户数据保存到数据库
            form.save()

            # 注册成功，跳转回首页
            return render(request, "注册成功")
    else:
        # 请求不是 POST，表明用户正在访问注册页面，展示一个空的注册表单给用户
        form = RegisterForm()

    # 渲染模板
    # 如果用户正在访问注册页面，则渲染的是一个空的注册表单
    # 如果用户通过表单提交注册信息，但是数据验证不合法，则渲染的是一个带有错误信息的表单
    return render(request, 'users/register.html', context={'form': form})


def index(request):
    return render(request, 'index.html')


# 返回新建病人信息页面
@login_required
def patient_regist(request):
    # form = PatientRegisterForm()
    try:
        if request.method == 'POST':
            try:
                care_id = request.POST["care_id"]
            except KeyError:
                care_id = "12345678910"
            name = request.POST["name"]
            try:
                sex = request.POST["sex"]
            except KeyError:
                sex = "male"
            id_num = request.POST["id_num"]
            birth = request.POST["birth"]
            phone_num = request.POST["phone_num"]
            address = request.POST["address"]
            try:
                nation = request.POST["nation"]
                marriage = request.POST["marriage"]
            except KeyError:
                nation = "0"
                marriage = "0"

            job = request.POST["job"]
            parent_name = request.POST["parent_name"]
            parent_real = request.POST["parent_real"]
            parent_phone = request.POST["parent_phone"]
            allergy = request.POST["allergy"]
            sickhis = request.POST["sickhis"]

            # 增加病人信息
            from his06.models import Patient
            person = Patient()
            person.care_id = care_id
            person.name = name
            person.sex = sex
            person.id_num = id_num
            person.birth = birth
            person.phone_num = phone_num
            person.address = address
            person.nation = nation
            person.marriage = marriage
            person.job = job
            person.parent_name = parent_name
            person.parent_real = parent_real
            person.parent_phone = parent_phone
            person.allergy = allergy
            person.sick_his = sickhis
            person.save()

            # 重定向到添加成功页面
            return render(request, 'validation.html')
    except:
        return render(request, "404.html")
    return render(request, "patient_regist.html")


# 根据用户登录的权限返回页面
@login_required
def nurse_index(request):
    if request.user.priority == "1":
        return render(request, 'validation.html')
    else:
        return render(request, "doctor_index.html")


# 返回病人挂号页面
@login_required
def patient_sign(request):
    error = ""
    obj = []
    super = models.Super.objects.all()
    if request.method == "POST":
        try:
            check_id = request.POST["care_id"]
            obj = models.Patient.objects.get(care_id=check_id)
            error = "该诊疗卡号存在，可以正常挂号！"
            return render(request, "patient_sign.html", context={"error": error, "obj": obj, "super": super})
        except models.Patient.DoesNotExist:
            error = "你查询的诊疗卡号不存在！"
            return render(request, "patient_sign.html", context={"error": error, "obj": obj, "super": super})
    return render(request, "patient_sign.html", context={"error": error, "obj": obj, "super": super})


# 返回查询病人信息的页面
@login_required
def patient_check(request):
    obj = []
    if request.method == "POST":
        try:
            check_id = request.POST["care_id"]
            from his06 import models
            obj = models.Patient.objects.get(care_id=check_id)
            return render(request, "patient_check.html", context={"obj": obj})
        except models.Patient.DoesNotExist:
            error = "你查询的诊疗卡号不存在！"
            obj = []
            return render(request, "patient_check.html", context={"obj": obj, "error": error})
    return render(request, "patient_check.html", context={"obj": obj})


# 根据大科室联动查询小科室
def get_department(request):
    pk = request.GET['pk']
    _super = get_object_or_404(models.Super, pk=pk)
    department = _super.department_set.all()
    data = serializers.serialize('json', department)
    return HttpResponse(data, content_type='application/json')


# 根据挂号科室联动展示医生职称
def get_level(request):
    pk = request.GET['pk']
    doc = models.Doctor.objects.filter(dep=pk)
    data = serializers.serialize('json', doc)
    return HttpResponse(data, content_type='application/json')


# 得到医生姓名
def get_doc_name(request):
    from datetime import datetime
    dep = request.GET['dep']
    pk = request.GET['id']
    my_date = request.GET['my_date']
    # inner_qs = models.WorkTime.objects.filter(work_date__date=datetime.today().date())
    my_date = datetime.strptime(my_date, "%Y-%m-%d")
    inner_qs = models.WorkTime.objects.filter(work_date=my_date)
    user = []
    for item in inner_qs:
        user.append(item.doc_id)
    doc_name = models.Doctor.objects.filter(_level=pk, dep=dep, username__in=user)
    print(doc_name)
    data = serializers.serialize('json', doc_name)
    return HttpResponse(data, content_type='application/json')


# 就诊房间查询
def get_room(request):
    name = request.GET['pk']
    doc_room = models.Doctor.objects.filter(username=name)
    data = serializers.serialize('json', doc_room)
    return HttpResponse(data, content_type='application/json')


# 获取医生的性别
def get_sex(request):
    name = request.GET['pk']
    doc_room = models.Doctor.objects.filter(username=name)
    data = serializers.serialize('json', doc_room)
    return HttpResponse(data, content_type='application/json')


# 提交挂号信息
def save_sign(request):
    try:
        if request.method == 'POST':
            water_id = request.POST['water_id']
            care_id = request.POST['care_id']
            patient_name = request.POST['patient_name']
            patient_sex = request.POST['patient_sex']
            patient_id = request.POST['patient_id']
            sign_time = request.POST['sign_time']
            patient_phone = request.POST['patient_phone']
            patient_address = request.POST['patient_address']
            super = request.POST['super']
            dep = request.POST['department']
            doc_level = request.POST['level']
            doc_name = request.POST['doc_name']
            doc_room = request.POST['room']
            doc_sex = request.POST['doc_sex']
            sign_kind = request.POST['sign_kind']
            is_book = request.POST['take_book']
            should_pay = request.POST['all_money']
            real_pay = request.POST['pay_money']
            ret_pay = request.POST['ret_money']
            care_num = request.POST['care_num']

            from his06.models import PatientSign
            patient = PatientSign()
            patient.water_id = water_id
            patient.patient_name = patient_name
            patient.care_id = care_id
            patient.patientSex = patient_sex
            patient.patient_id = patient_id
            patient.patient_phone = patient_phone
            patient.patient_address = patient_address
            patient.super = super
            patient.dep = dep
            patient.doc_level = doc_level
            patient.doc_name = doc_name
            patient.doc_room = doc_room
            patient.doc_sex = doc_sex
            patient.sign_kind = sign_kind
            patient.is_book = is_book
            patient.should_pay = should_pay
            patient.real_pay = real_pay
            patient.ret_pay = ret_pay
            patient.sign_time = sign_time
            patient.care_num = care_num

            patient.save()
            # 糟了...这里出问题了..
            # 将挂号医生对应的剩下诊疗号减少
            doc = models.Doctor.objects.filter(username=doc_name)
            doc.update(num_left=doc[0].num_left - 1)
            # doc = models.Doctor(username=doc_name)
            # _doc[0].num_left = _doc[0].num_left - 1
            # _doc.save(force_update=True)
            # doc.num_left = doc.num_left - 1
            # doc.save(update_fields=['num_left'])

            num = models.WaterNum.objects.filter(pk=water_id)
            num.update(id=num[0].id + 1)
            # num.id = int(water_id) + 1
            # num.save(force_update=True)

            return render(request, 'validation.html')
    except:
        return render(request, "404.html")


# 获取流水号
def get_water_num(request):
    water_id = models.WaterNum.objects.all()
    data = serializers.serialize('json', water_id)
    return HttpResponse(data, content_type='application/json')


# 获取诊疗号(已经不需要了,使用上面的get_sex同样能得到需要的数据,就复用了那个函数)
def get_order_num(request):
    pass


def doc_work_time(request):
    error = ""
    obj = []
    if request.method == "POST":
        try:
            pk = request.POST['doc_id']
            obj = models.WorkTime.objects.filter(doc_id=pk)
            return render(request, "doc_work_time.html", context={"error": error, "item": obj})
        except models.WorkTime.DoesNotExist:
            error = "你查询的工号不存在！"
            return render(request, "doc_work_time.html", context={"error": error, "item": obj})
    return render(request, 'doc_work_time.html')


def doc_check(request):
    import datetime
    error = ""
    obj = []
    try:
        date = datetime.datetime.now(tz=timezone.utc) + timedelta(days=-2)
        it = models.PatientSign.objects.filter(sign_time__gte=date, is_deal=0, doc_room=request.user.room)
        return render(request, "doc_check.html", context={"error": error, "item": it})
    except models.PatientSign.DoesNotExist:
        return render(request, "doc_check.html", context={"error": error, "item": obj})


@login_required
def patient_detail(request):
    obj = []
    doc = []
    if request.method == 'GET':
        try:
            check_id = request.GET["pk"]
            obj = models.PatientSign.objects.get(water_id=int(check_id))
            care_id = obj.care_id
            doc = models.Patient.objects.get(care_id=care_id)
            medicine = models.MedicineType.objects.all()
            return render(request, "patient_detail.html", context={"obj": obj, "doc": doc, "medicine": medicine})
        except models.Patient.DoesNotExist:
            pass


def get_medicine_kind(request):
    pk = request.GET['pk']
    _super = get_object_or_404(models.MedicineType, pk=pk)
    department = _super.medicinekind_set.all()
    data = serializers.serialize('json', department)
    return HttpResponse(data, content_type='application/json')


def get_medicine_name(request):
    pk = request.GET['pk']
    doc = models.Medicine.objects.filter(sm_id=pk)
    data = serializers.serialize('json', doc)
    return HttpResponse(data, content_type='application/json')


def get_max_num(request):
    pk = request.GET['pk']
    doc = models.Medicine.objects.filter(medicineId=pk)
    data = serializers.serialize('json', doc)
    return HttpResponse(data, content_type='application/json')


def save_sick_his(request):
    from datetime import datetime
    try:
        if request.method == 'POST':
            water_id = request.POST['water_id']
            care_id = request.POST['care_id']
            symtop = request.POST['symtop']
            result = request.POST['care_result']
            medi_use = request.POST['med']
            list = request.POST.getlist('check_pro')
            check_pro = ','.join(list)

            from his06.models import Sick_his
            sick_item = Sick_his()
            sick_item.sick_id = water_id
            sick_item.care_id = care_id
            sick_item.sick_symtop = symtop
            sick_item.result = result
            sick_item.medi_use = medi_use
            sick_item.sick_pro = check_pro

            sick_item.save()

            pa = models.PatientSign.objects.filter(water_id=water_id)
            pa.update(is_deal=1)

            si = models.Patient.objects.filter(care_id=care_id)
            pro = []
            for li in list:
                if(li == "01"):
                    pro.append("B超")
                elif(li == "02"):
                    pro.append("CR")
                elif(li == "03"):
                    pro.append("DR")
                elif(li == "04"):
                    pro.append("CT")
                elif(li == "05"):
                    pro.append("MRI")
                elif(li == "06"):
                    pro.append("DSA")
            pro_text = ','.join(pro)
            str = si[0].sick_his
            str = str+"就诊时间："+datetime.today().date().strftime('%Y-%m-%d')+"\n症状描述："+symtop+"\n诊疗结果："+result+"\n用药处方："+medi_use+"就诊项目"+pro_text+"\n"
            si.update(sick_his=str)
            return render(request, 'doctor_index.html')
    except:
        return render(request, "404.html")


def get_id_num(request):
    data = models.Patient.objects.all()
    data = serializers.serialize('json', data)
    return HttpResponse(data, content_type='application/json')


def patient_update(request):
    try:
        if request.method == "POST":
            care_id = request.POST['care_id']
            name = request.POST['name']
            sex = request.POST['sex']
            phone = request.POST['phone']
            address = request.POST['address']
            nation = request.POST['nation']
            marriage = request.POST['marriage']
            job = request.POST['job']
            parent_name = request.POST['parent_name']
            parent_real = request.POST['parent_real']
            parent_phone = request.POST['parent_phone']
            allergy_his = request.POST['allergy_his']

            pat = models.Patient.objects.filter(care_id=care_id)
            pat.update(name=name)
            pat.update(sex=sex)
            pat.update(phone_num=phone)
            pat.update(address=address)
            pat.update(nation=nation)
            pat.update(marriage=marriage)
            pat.update(job=job)
            pat.update(parent_name=parent_name)
            pat.update(parent_real=parent_real)
            pat.update(parent_phone=parent_phone)
            pat.update(allergy=allergy_his)
            return render(request, 'validation.html')
    except:
        return render(request, "404.html")


def check_doc_patient(request):
    pass

