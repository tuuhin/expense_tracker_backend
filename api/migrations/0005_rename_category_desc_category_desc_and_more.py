# Generated by Django 4.0.2 on 2022-02-16 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_category_category_desc_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='category_desc',
            new_name='desc',
        ),
        migrations.RenameField(
            model_name='category',
            old_name='category_title',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='expenses',
            old_name='expense_desc',
            new_name='desc',
        ),
        migrations.RenameField(
            model_name='expenses',
            old_name='expense_title',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='income',
            old_name='income_desc',
            new_name='desc',
        ),
        migrations.RenameField(
            model_name='income',
            old_name='income_title',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='source',
            old_name='source_desc',
            new_name='desc',
        ),
        migrations.RenameField(
            model_name='source',
            old_name='source_title',
            new_name='title',
        ),
        migrations.RemoveField(
            model_name='expenses',
            name='expense_amount',
        ),
        migrations.RemoveField(
            model_name='income',
            name='income_amount',
        ),
        migrations.AddField(
            model_name='expenses',
            name='amount',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='income',
            name='amount',
            field=models.FloatField(default=0),
        ),
    ]