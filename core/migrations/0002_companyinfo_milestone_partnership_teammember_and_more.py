# Generated by Django 5.0.2 on 2025-05-06 14:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mission', models.TextField(help_text="Company's mission statement")),
                ('vision', models.TextField(help_text="Company's vision statement")),
                ('history', models.TextField(help_text="Company's history and background")),
                ('established_date', models.DateField()),
            ],
            options={
                'verbose_name_plural': 'Company Information',
            },
        ),
        migrations.CreateModel(
            name='Milestone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('icon', models.CharField(blank=True, help_text='Font Awesome icon class', max_length=50)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ['order', 'date'],
            },
        ),
        migrations.CreateModel(
            name='Partnership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('company', 'IT Company'), ('certification', 'Certification Body'), ('academic', 'Academic Institution')], max_length=20)),
                ('logo', models.ImageField(upload_to='partners/')),
                ('description', models.TextField()),
                ('website_url', models.URLField()),
                ('partnership_date', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Partnerships',
                'ordering': ['order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('role', models.CharField(choices=[('instructor', 'Instructor'), ('management', 'Management'), ('support', 'Support Staff')], max_length=20)),
                ('designation', models.CharField(max_length=100)),
                ('photo', models.ImageField(blank=True, upload_to='team/')),
                ('bio', models.TextField()),
                ('qualifications', models.TextField()),
                ('achievements', models.TextField()),
                ('linkedin_url', models.URLField(blank=True)),
                ('github_url', models.URLField(blank=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_key_member', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Certification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('logo', models.ImageField(upload_to='certifications/')),
                ('validity_period', models.PositiveIntegerField(blank=True, help_text='Validity in months', null=True)),
                ('is_featured', models.BooleanField(default=False)),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certifications', to='core.partnership')),
            ],
        ),
    ]
