# Generated by Django 2.0 on 2018-05-19 17:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('his06', '0002_auto_20180520_0104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='dep',
            field=models.ForeignKey(db_column='dep_id', default='00101', on_delete=django.db.models.deletion.DO_NOTHING, to='his06.Department', verbose_name='所属科室'),
        ),
    ]
