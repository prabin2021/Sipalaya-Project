from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import BlogPost, Category, Tag, Comment

def blog_list(request):
    posts = BlogPost.objects.filter(status='published')
    categories = Category.objects.all()
    
    # Search functionality
    search_query = request.GET.get('q')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(excerpt__icontains=search_query)
        )
    
    # Category filter
    current_category = request.GET.get('category')
    if current_category:
        posts = posts.filter(category__slug=current_category)
    
    # Pagination
    paginator = Paginator(posts, 9)  # Show 9 posts per page
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'current_category': current_category,
        'search_query': search_query,
    }
    return render(request, 'blog/list.html', context)

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, status='published')
    post.increment_views()
    
    # Get related posts
    related_posts = BlogPost.objects.filter(
        category=post.category,
        status='published'
    ).exclude(id=post.id)[:3]
    
    # Handle comment submission
    if request.method == 'POST' and request.user.is_authenticated:
        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                post=post,
                author=request.user,
                content=content
            )
            messages.success(request, 'Your comment has been added.')
            return redirect('blog:detail', slug=post.slug)
    
    context = {
        'post': post,
        'related_posts': related_posts,
    }
    return render(request, 'blog/detail.html', context)

@login_required
def blog_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category_id = request.POST.get('category')
        content = request.POST.get('content')
        excerpt = request.POST.get('excerpt')
        meta_description = request.POST.get('meta_description')
        meta_keywords = request.POST.get('meta_keywords')
        status = request.POST.get('status')
        
        post = BlogPost.objects.create(
            title=title,
            author=request.user,
            category_id=category_id,
            content=content,
            excerpt=excerpt,
            meta_description=meta_description,
            meta_keywords=meta_keywords,
            status=status
        )
        
        # Handle featured image
        if 'featured_image' in request.FILES:
            post.featured_image = request.FILES['featured_image']
            post.save()
        
        messages.success(request, 'Blog post created successfully.')
        return redirect('blog:detail', slug=post.slug)
    
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'blog/create.html', context)

@login_required
def blog_edit(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    
    # Check if user is the author
    if post.author != request.user:
        messages.error(request, 'You do not have permission to edit this post.')
        return redirect('blog:detail', slug=post.slug)
    
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.category_id = request.POST.get('category')
        post.content = request.POST.get('content')
        post.excerpt = request.POST.get('excerpt')
        post.meta_description = request.POST.get('meta_description')
        post.meta_keywords = request.POST.get('meta_keywords')
        post.status = request.POST.get('status')
        
        # Handle featured image
        if 'featured_image' in request.FILES:
            post.featured_image = request.FILES['featured_image']
        
        post.save()
        messages.success(request, 'Blog post updated successfully.')
        return redirect('blog:detail', slug=post.slug)
    
    categories = Category.objects.all()
    context = {
        'post': post,
        'categories': categories,
    }
    return render(request, 'blog/edit.html', context)

@login_required
def blog_delete(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    
    # Check if user is the author
    if post.author != request.user:
        messages.error(request, 'You do not have permission to delete this post.')
        return redirect('blog:detail', slug=post.slug)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Blog post deleted successfully.')
        return redirect('blog:list')
    
    context = {
        'post': post,
    }
    return render(request, 'blog/delete.html', context)
