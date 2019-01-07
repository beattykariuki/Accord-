from django.conf import settings
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.conf.urls import url,include
from django.contrib.auth import authenticate,login,logout
from .forms import PostForm,CommentForm
from django.conf.urls.static import static
from .models import Profile,Image,Likes
from django.contrib.auth.models import User
from annoying.decorators import ajax_request

from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .models import Comments

# Create your views here.
def welcome(request):
    return HttpResponse('Welcome to Instagram')

@login_required(login_url='/accounts/login')
def index(request):
    all_images = Image.objects.all()
    all_users = Profile.objects.all()
    likes = Likes.objects.all()
    next = request.GET.get('next')
    if request.method == 'POST':
       form = CommentForm(request.POST)
       image_id = int(request.POST.get("betty"))
       post = Image.objects.get(id = image_id)
       if form.is_valid():
           comment = form.save(commit=False)
           comment.post = post
           comment.author = request.user
           comment.save()
           return redirect('index')
    else:
        form = CommentForm()
    if next:return redirect(next)
    return render(request, 'showcase/home.html', {"all_images": all_images,"all_users":all_users,'form':form})

@login_required(login_url='/accounts/login/')
def explore(request):
    return render(request, 'showcase/explore.html')

@login_required(login_url='/accounts/login/')
def notification(request):
    return render(request, 'showcase/notification.html')

def logout(request):
    return render(request, 'registration/logout.html')

def login(request):
    return render(request, 'registration/login.html')

@login_required(login_url='/accounts/login/')
def upload(request):
    current_user = request.user
    p = Profile.objects.filter(id=current_user.id).first()
    imageuploader_profile = Image.objects.filter(imageuploader_profile=p).all()
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.imageuploader_profile= p
            post.save()
            return redirect('/')
    else:
        form =PostForm
    return render(request, 'showcase/upload.html', {"form": form})

@login_required(login_url='/accounts/login/')
def like(request, image_id):
    image = get_object_or_404(Image, pk=image_id)
    request.user.profile.like(image)
    return JsonReponse(image.count_likes, safe=False)

@login_required(login_url='/accounts/login/')
def unlike(request, image_id):
    image = get_object_or_404(Image, pk=post_id)
    request.user.profile.unlike(image)
    return JsonReponse(image.count_likes, safe=False)

    

def profile(request):
    return render(request,'showcase/profile.html')

def add_comment_to_post(request):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
       form = CommentForm(request.POST)
       if form.is_valid():
           comment = form.save(commit=False)
           comment.post =post
           comment.save()
           return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'image/add_comment_to_home.html', {'form': form})

def approve(self):
    self.approved_comment = True
    self.save()
