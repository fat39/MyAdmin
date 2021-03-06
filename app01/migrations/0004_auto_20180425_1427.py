# Generated by Django 2.0.1 on 2018-04-25 06:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_auto_20180424_2227'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='mmm',
        ),
        migrations.AddField(
            model_name='userinfo',
            name='role',
            field=models.ManyToManyField(to='app01.Role', verbose_name='角色'),
        ),
        migrations.AlterField(
            model_name='usergroup',
            name='title',
            field=models.CharField(max_length=32, verbose_name='用户组'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='ug',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.UserGroup', verbose_name='用户组'),
        ),
    ]
