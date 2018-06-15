from django.conf.urls import url
from . import views

app_name = 'his06'
urlpatterns = [
    url(r'^register/', views.register, name='register'),
    url(r'^nurse_index/$', views.nurse_index, name='nurse'),
    url(r'^patient_sign/$', views.patient_sign, name='patient_sign'),
    url(r'^patient_regist/$', views.patient_regist, name='patient_reg'),
    url(r'^patient_check/$', views.patient_check, name="patient_check"),
    url(r'^get_department/$', views.get_department, name='get_department'),
    url(r'^get_level/$', views.get_level, name='get_level'),
    url(r'^get_doc_name/$', views.get_doc_name, name='get_doc_name'),
    url(r'^get_room/$', views.get_room, name='get_room'),
    url(r'^get_sex/$', views.get_sex, name="get_sex"),
    url(r'^save_sign/', views.save_sign, name='save_sign'),
    url(r'^get_water_num/', views.get_water_num, name='get_water_num'),
    url(r'^get_order_num/', views.get_order_num, name='get_order_num'),
    url(r'^doc_work_time/', views.doc_work_time, name='doc_work_time'),
    url(r'^doc_check/', views.doc_check, name='doc_check'),
    url(r'^patient_detail/', views.patient_detail, name='patient_detail'),
    url(r'^get_medicine_kind/', views.get_medicine_kind, name='get_medicine_kind'),
    url(r'^get_medicine_name/', views.get_medicine_name, name='get_medicine_name'),
    url(r'get_max_num/', views.get_max_num, name='get_max_num'),
    url(r'^save_sick_his/', views.save_sick_his, name='save_sick_his'),
    url(r'^get_id_num/', views.get_id_num, name='get_id_num'),
    url(r'patient_update/', views.patient_update, name='patient_update'),
    url(r'check_doc_patient/', views.check_doc_patient, name='check_doc_patient'),
]
