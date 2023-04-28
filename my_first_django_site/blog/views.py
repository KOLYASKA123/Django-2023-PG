from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseForbidden
from django.views.generic import ListView, UpdateView
from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post, Category
from blog.forms import EmailPostForm, CommentForm, NewPostForm, NewCategoryForm, EditPostForm
from django.core.mail import send_mail
from django.db.models import Count
from taggit.models import Tag
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib import messages


# Create your views here.

# def post_list(request):
#     object_list = Post.objects.filter(status=Post.PostStatus.PUBLISHED)
#     paginator = Paginator(object_list, 3)
#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#     return render(
#         request,
#         'blog/post/list.html',
#         {'page': page,
#         'posts': posts})

# class PostListView(ListView):

#     queryset = Post.objects.filter(status=Post.PostStatus.PUBLISHED)
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'blog/post/list.html'

def post_list(request, tag_slug=None):
    object_list = Post.objects.filter(status=Post.PostStatus.PUBLISHED)
    tag = None

    if tag_slug:

        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(
        request, 
        'blog/post/list.html', 
        {'page': page,
        'posts': posts,
        'tag': tag})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.filter(active=True)
    am_I_the_author = request.user == post.author

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(status=Post.PostStatus.PUBLISHED).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form, 'similar_posts': similar_posts, 'am_I_the_author': am_I_the_author})

def post_share(request, post_id):
    
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':

        form = EmailPostForm(request.POST)

        if form.is_valid():

            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:

        form = EmailPostForm()

    return render(
        request, 
        'blog/post/share.html', 
        {'post': post,
        'form': form,
        'sent': sent})
    
@login_required
def create_post(request):
    
    if not(request.user.is_authenticated): 
        
        print('Не авторизирован')    
        return redirect('users:login')
    
    else:
        
        category_form = NewCategoryForm(request.POST)
        post_form = NewPostForm(request.POST)
        
        if request.user.is_superuser:

            if request.method == 'POST':
                
                if 'create_category' in request.POST:
                    
                    category_form = NewCategoryForm(request.POST)
                    
                    if category_form.is_valid():
                        
                        category = category_form.save(commit=False)
                        category.author = request.user
                        category.save()
                        
                elif 'create_post' in request.POST:
                    
                    post_form = NewPostForm(request.POST, request.FILES, user=request.user)
                    
                    if post_form.is_valid():
                        
                        news = post_form.save(commit=False)
                        news.image = request.FILES.get('image')
                        news.author = request.user
                        news.tag = request.POST.get('tag')
                        news.slug = request.POST.get('slug')
                        news.save()
                        news.tags.set(post_form.cleaned_data['tags'])
                        return redirect('blog:post_list')
            else:

                post_form = NewPostForm(user=request.user)

            return render(request, 'blog/post/create_post.html', {'category_form': category_form, 'post_form': post_form})

        else:

            return HttpResponseForbidden()

@login_required
def edit_post(request, post_id):
    
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        
        form = EditPostForm(request.POST, request.FILES, instance=post, user = request.user)
        
        if form.is_valid():
            
            news = form.save(commit=False)
            news.image = request.FILES.get('image')
            news.author = request.user
            news.tag = request.POST.get('tag')
            news.slug = request.POST.get('slug')
            news.save()
            news.tags.set(form.cleaned_data['tags'])
            
            return redirect('blog:post_detail', post_id=post_id)
    else:
        
        form = EditPostForm(instance=post, user=request.user)
    
    return render(request, 'blog/post/edit_post.html', {'form': form, 'post_id': post_id})

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully.')
        return redirect('blog:post_list')

    #return render(request, 'blog/post/delete_post.html', {'post_id': post_id})

class BlogListView(LoginRequiredMixin, ListView):
    
    model = Category
    template_name = 'blog/post/my_blogs.html'  # имя вашего шаблона
    context_object_name = 'blogs'
    login_url = 'accounts/login/'
    
    def get(self, request):
        # Получаем авторизованного пользователя
        user = request.user
        # Получаем все блоги, принадлежащие данному пользователю
        blogs = Category.objects.filter(author=user)
        context = {'blogs': blogs}  # Передаем список блогов в контекст шаблона
        return render(request, self.template_name, context)
    
def posts_of_blog(request, blog_id, tag_slug=None):
    
    blog = get_object_or_404(Category, id=blog_id)
    posts = Post.objects.filter(category=blog)
    tag = None

    if tag_slug:

        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    context = {'blog': blog, 'page': page, 'posts': posts, 'tag': tag}
    return render(request, 'blog/post/posts_of_blog.html', context)
    