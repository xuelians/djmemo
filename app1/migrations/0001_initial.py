# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-22 06:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='Title')),
                ('author', models.CharField(max_length=16, verbose_name='Author')),
                ('content', models.TextField(verbose_name='Text')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
            ],
        ),
        migrations.CreateModel(
            name='Bug',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bugno', models.CharField(max_length=16, verbose_name='Bug')),
                ('desc', models.CharField(max_length=256, verbose_name='Description')),
                ('comment', models.CharField(blank=True, max_length=256, verbose_name='Comment')),
                ('status', models.CharField(choices=[('new', 'Assign'), ('wrk', 'Work-on'), ('rca', 'Root Cause'), ('sol', 'Solution'), ('qat', 'QA Test'), ('eco', 'ECO Submit'), ('fix', 'Fixed'), ('pen', 'Pending')], max_length=16, verbose_name='Status')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Last modified')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, verbose_name='Text')),
            ],
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='Title')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, verbose_name='Name')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('content', models.CharField(max_length=140, verbose_name='Text')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.Blog', verbose_name='Blog')),
            ],
        ),
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bug_enable', models.BooleanField(default=False, verbose_name='Enable Bug List')),
                ('task_enable', models.BooleanField(default=False, verbose_name='Enable Task List')),
                ('note_enable', models.BooleanField(default=False, verbose_name='Enable Note List')),
            ],
        ),
        migrations.CreateModel(
            name='Memo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='Title')),
                ('author', models.CharField(max_length=32, verbose_name='Author')),
                ('summary', models.TextField(verbose_name='Summary')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Last modified')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.Category', verbose_name='Category')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keypoint', models.CharField(blank=True, max_length=256, verbose_name='Key Point')),
                ('content', models.TextField(verbose_name='Text')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Last modified')),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.Chapter', verbose_name='Chapter')),
                ('memo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.Memo', verbose_name='Memo')),
            ],
        ),
        migrations.CreateModel(
            name='SectionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, verbose_name='Text')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, verbose_name='Text')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('started', models.DateField(verbose_name='Started')),
                ('eta', models.DateField(verbose_name='ETA')),
                ('bug', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.Bug', verbose_name='Bug')),
            ],
        ),
        migrations.CreateModel(
            name='TaskUpdate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complete', models.PositiveSmallIntegerField(verbose_name='complete')),
                ('hours', models.PositiveSmallIntegerField(verbose_name='Hours')),
                ('comment', models.CharField(max_length=256, verbose_name='Comment')),
                ('updated', models.DateField(auto_now_add=True, verbose_name='Updated')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.Task', verbose_name='Task')),
            ],
        ),
        migrations.AddField(
            model_name='section',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.SectionType', verbose_name='Type'),
        ),
        migrations.AddField(
            model_name='memo',
            name='tag',
            field=models.ManyToManyField(to='app1.Tag', verbose_name='Tag'),
        ),
        migrations.AddField(
            model_name='chapter',
            name='memo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.Memo', verbose_name='Memo'),
        ),
        migrations.AddField(
            model_name='bug',
            name='memo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.Memo', verbose_name='Memo'),
        ),
        migrations.AddField(
            model_name='blog',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.Category', verbose_name='Category'),
        ),
        migrations.AddField(
            model_name='blog',
            name='tags',
            field=models.ManyToManyField(to='app1.Tag', verbose_name='Tag'),
        ),
    ]
