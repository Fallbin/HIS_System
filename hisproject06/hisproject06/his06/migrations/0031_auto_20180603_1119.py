# Generated by Django 2.0 on 2018-06-03 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('his06', '0030_auto_20180603_0355'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientsign',
            name='is_deal',
            field=models.BooleanField(db_column='is_deal', default=0, verbose_name='是否处理'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='care_id',
            field=models.CharField(db_column='care_id_num', default='20180603719174', error_messages={0: '该诊疗卡号不存在'}, max_length=255, primary_key=True, serialize=False, verbose_name='诊疗卡号'),
        ),
    ]