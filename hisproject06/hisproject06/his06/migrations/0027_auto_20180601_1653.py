# Generated by Django 2.0 on 2018-06-01 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('his06', '0026_auto_20180601_0225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='room',
            field=models.CharField(blank=True, db_column='doc_room', default='A栋403', max_length=255, verbose_name='科室房间'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='care_id',
            field=models.CharField(db_column='care_id_num', default='20180601787439', error_messages={0: '该诊疗卡号不存在'}, max_length=255, primary_key=True, serialize=False, verbose_name='诊疗卡号'),
        ),
    ]