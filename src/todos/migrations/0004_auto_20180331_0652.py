# Generated by Django 2.0.2 on 2018-03-31 03:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0003_tag'),
    ]

    operations = [
        migrations.AlterOrderWithRespectTo(
            name='todo',
            order_with_respect_to='todolist',
        ),
    ]
