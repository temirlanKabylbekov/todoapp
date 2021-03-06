# Generated by Django 2.0.2 on 2018-03-22 10:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0002_todo_todolist'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('todo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='todos.Todo')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
