# Generated by Django 4.0.4 on 2022-05-19 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('librarysystem', '0002_user_is_member'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issuedbooks',
            name='issued_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]