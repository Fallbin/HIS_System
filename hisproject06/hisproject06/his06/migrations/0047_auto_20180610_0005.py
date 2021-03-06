# Generated by Django 2.0 on 2018-06-09 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('his06', '0046_auto_20180609_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='care_id',
            field=models.CharField(db_column='care_id_num', default='20180610645074', error_messages={0: '该诊疗卡号不存在'}, max_length=255, primary_key=True, serialize=False, verbose_name='诊疗卡号'),
        ),
        migrations.AlterField(
            model_name='patientsign',
            name='doc_level',
            field=models.CharField(db_column='doc_level', max_length=255, verbose_name='医生职称'),
        ),
    ]
