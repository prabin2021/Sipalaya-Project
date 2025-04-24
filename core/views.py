from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Banner, Feature, Testimonial, FAQ, Contact, SiteSetting
from .forms import ContactForm
from courses.models import Course

class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['banners'] = Banner.objects.filter(is_active=True).order_by('order')
        context['features'] = Feature.objects.all().order_by('order')
        context['popular_courses'] = Course.objects.filter(is_published=True).order_by('-created_at')[:6]
        context['testimonials'] = Testimonial.objects.filter(is_active=True).order_by('order')
        return context

class AboutView(TemplateView):
    template_name = 'about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['features'] = Feature.objects.all().order_by('order')
        context['testimonials'] = Testimonial.objects.filter(is_active=True).order_by('order')
        return context

class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/contact/'
    
    def form_valid(self, form):
        contact = form.save()
        messages.success(self.request, 'Your message has been sent successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_settings'] = SiteSetting.objects.first()
        return context

class FAQView(ListView):
    template_name = 'faq.html'
    context_object_name = 'faqs'
    model = FAQ
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = FAQ.objects.values_list('category', flat=True).distinct()
        return context

class StudentDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'student_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enrolled_courses'] = self.request.user.enrollments.filter(is_active=True)
        context['completed_courses'] = self.request.user.enrollments.filter(completed_at__isnull=False)
        return context

class InstructorDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'instructor_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = self.request.user.courses.all()
        context['total_students'] = sum(course.enrollments.count() for course in context['courses'])
        return context

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context 