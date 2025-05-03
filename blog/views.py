from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Blog, Category
from django.db.models import Q

def blog_list(request):
    category = request.GET.get('category')
    search_query = request.GET.get('q')
    
    blogs = Blog.objects.filter(is_published=True)
    
    if category:
        blogs = blogs.filter(category__slug=category)
    
    if search_query:
        blogs = blogs.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    
    categories = Category.objects.all()
    
    # Pagination
    paginator = Paginator(blogs, 9)  # Show 9 posts per page
    page = request.GET.get('page')
    blogs = paginator.get_page(page)
    
    context = {
        'blogs': blogs,
        'categories': categories,
        'current_category': category,
        'search_query': search_query
    }
    return render(request, 'blog/blog_list.html', context)

def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug, is_published=True)
    blog.increase_views()
    
    # Get related posts
    related_posts = Blog.objects.filter(
        category=blog.category,
        is_published=True
    ).exclude(id=blog.id)[:3]
    
    context = {
        'blog': blog,
        'related_posts': related_posts
    }
    return render(request, 'blog/blog_detail.html', context)

@login_required
def create_blog(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to create blog posts.')
        return redirect('blog:blog_list')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category_id = request.POST.get('category')
        featured_image = request.FILES.get('featured_image')
        meta_description = request.POST.get('meta_description')
        meta_keywords = request.POST.get('meta_keywords')
        
        try:
            category = Category.objects.get(id=category_id)
            blog = Blog.objects.create(
                title=title,
                content=content,
                author=request.user,
                category=category,
                featured_image=featured_image,
                meta_description=meta_description,
                meta_keywords=meta_keywords,
                is_published=False  # Default to draft
            )
            messages.success(request, 'Blog post created successfully and is pending approval.')
            return redirect('blog:blog_detail', slug=blog.slug)
        except Exception as e:
            messages.error(request, f'Error creating blog post: {str(e)}')
    
    categories = Category.objects.all()
    return render(request, 'blog/create_blog.html', {'categories': categories})

@login_required
def edit_blog(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    
    if not request.user.is_staff and request.user != blog.author:
        messages.error(request, 'You do not have permission to edit this post.')
        return redirect('blog:blog_detail', slug=slug)
    
    if request.method == 'POST':
        blog.title = request.POST.get('title')
        blog.content = request.POST.get('content')
        blog.category_id = request.POST.get('category')
        blog.meta_description = request.POST.get('meta_description')
        blog.meta_keywords = request.POST.get('meta_keywords')
        
        if request.FILES.get('featured_image'):
            blog.featured_image = request.FILES['featured_image']
        
        blog.save()
        messages.success(request, 'Blog post updated successfully.')
        return redirect('blog:blog_detail', slug=blog.slug)
    
    categories = Category.objects.all()
    return render(request, 'blog/edit_blog.html', {
        'blog': blog,
        'categories': categories
    })
