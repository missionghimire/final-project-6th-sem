# Generated by Django 4.0.4 on 2022-05-27 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0002_passwordreset_remove_customuser_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100)),
                ('Email', models.EmailField(max_length=100)),
                ('numbers', models.CharField(max_length=100)),
                ('message', models.TextField(max_length=100)),
            ],
        ),
    ]
