# Generated by Django 4.1.1 on 2022-09-28 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_rename_sentence_sentence_ar_sentence_groups_ar_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groups',
            name='words',
            field=models.ManyToManyField(blank=True, null=True, to='pages.words'),
        ),
    ]