from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from .models import Category, Course, Module, Lesson, Enrollment, Progress, Review
from .forms import CourseForm, ModuleForm, LessonForm, ReviewForm

class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = Course.objects.filter(is_published=True)
        category = self.request.GET.get('category')
        level = self.request.GET.get('level')
        search = self.request.GET.get('search')
        
        if category:
            queryset = queryset.filter(category__slug=category)
        if level:
            queryset = queryset.filter(level=level)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(tags__name__icontains=search)
            ).distinct()
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['levels'] = Course.objects.values_list('level', flat=True).distinct()
        return context

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_enrolled'] = Enrollment.objects.filter(
                student=self.request.user,
                course=self.object,
                is_active=True
            ).exists()
        return context

class CourseEnrollView(LoginRequiredMixin, CreateView):
    model = Enrollment
    template_name = 'courses/course_enroll.html'
    fields = []
    
    def form_valid(self, form):
        course = get_object_or_404(Course, slug=self.kwargs['slug'])
        form.instance.student = self.request.user
        form.instance.course = course
        messages.success(self.request, 'Successfully enrolled in the course!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('courses:course_detail', kwargs={'slug': self.kwargs['slug']})

class CourseLearnView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'courses/course_learn.html'
    context_object_name = 'course'
    
    def get_object(self):
        course = super().get_object()
        if not Enrollment.objects.filter(
            student=self.request.user,
            course=course,
            is_active=True
        ).exists():
            messages.error(self.request, 'You are not enrolled in this course!')
            return redirect('courses:course_detail', slug=course.slug)
        return course
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        enrollment = Enrollment.objects.get(
            student=self.request.user,
            course=self.object,
            is_active=True
        )
        context['enrollment'] = enrollment
        context['progress'] = Progress.objects.filter(enrollment=enrollment)
        return context

class CourseReviewView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'courses/course_review.html'
    
    def form_valid(self, form):
        course = get_object_or_404(Course, slug=self.kwargs['slug'])
        enrollment = get_object_or_404(
            Enrollment,
            student=self.request.user,
            course=course,
            is_active=True
        )
        form.instance.enrollment = enrollment
        messages.success(self.request, 'Thank you for your review!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('courses:course_detail', kwargs={'slug': self.kwargs['slug']})

class InstructorCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'courses/instructor_course_list.html'
    context_object_name = 'courses'
    
    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)

class InstructorCourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/instructor_course_form.html'
    
    def form_valid(self, form):
        form.instance.instructor = self.request.user
        messages.success(self.request, 'Course created successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('courses:instructor_course_list')

class InstructorCourseUpdateView(LoginRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/instructor_course_form.html'
    
    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Course updated successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('courses:instructor_course_list')

class InstructorCourseDeleteView(LoginRequiredMixin, DeleteView):
    model = Course
    template_name = 'courses/instructor_course_confirm_delete.html'
    
    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Course deleted successfully!')
        return super().delete(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('courses:instructor_course_list') 