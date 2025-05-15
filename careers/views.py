from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PlacementService, CompanyPartnership, JobListing, AlumniSuccessStory, JobApplication
from .forms import JobApplicationForm

def placement_services(request):
    """View for displaying placement services and company partnerships."""
    services = PlacementService.objects.all()
    partnerships = CompanyPartnership.objects.all()
    
    context = {
        'services': services,
        'partnerships': partnerships,
    }
    return render(request, 'careers/placement_services.html', context)

def job_listings(request):
    """View for displaying active job listings."""
    jobs = JobListing.objects.filter(
        is_active=True,
        application_deadline__gte=timezone.now().date()
    ).select_related('company').order_by('application_deadline')
    
    context = {
        'jobs': jobs,
    }
    return render(request, 'careers/job_listings.html', context)

def alumni_stories(request):
    """View for displaying alumni success stories."""
    stories = AlumniSuccessStory.objects.all().order_by('-graduation_year')
    
    context = {
        'stories': stories,
    }
    return render(request, 'careers/alumni_stories.html', context)

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(JobListing, id=job_id, is_active=True)
    
    # Check if user has already applied
    if JobApplication.objects.filter(job=job, applicant=request.user).exists():
        messages.error(request, 'You have already applied for this position.')
        return redirect('careers:job_listings')
    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            messages.success(request, 'Your application has been submitted successfully!')
            return redirect('careers:job_listings')
    else:
        form = JobApplicationForm()
    
    return render(request, 'careers/apply_job.html', {
        'form': form,
        'job': job
    })
