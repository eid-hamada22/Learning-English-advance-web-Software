# Generated by Django 4.1.1 on 2022-10-20 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0009_groups_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='groups',
            name='book',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='groups',
            name='words',
            field=models.ManyToManyField(blank=True, to='pages.words'),
        ),
    ]
