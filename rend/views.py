from django.conf import settings
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.conf.urls import url,include
from django.contrib.auth import authenticate,login,logout
from .forms import PostForm,CommentForm
from django.conf.urls.static import static
from .models import Profile,Project,Comments,Review
from django.contrib.auth.models import User
from annoying.decorators import ajax_request

from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.db.models import Avg

# Create your views here.
def welcome(request):
    return HttpResponse('Welcome to Renditt')

@login_required(login_url='/accounts/login')
def index(request):
    all_projects = Project.objects.all()
    print(all_projects)
    all_users = Profile.objects.all()
    comments = Comments.objects.all() 
    next = request.GET.get('next')
    if request.method == 'POST':
       form = CommentForm(request.POST)
       image_id = int(request.POST.get("betty"))
       post = Project.objects.get(id = image_id)
       if form.is_valid():
           comment = form.save(commit=False)
           comment.post = post
           comment.author = request.user
           comment.save()
           return redirect('index')
    else:
        form = CommentForm()
    if next:return redirect(next)
    return render(request, 'showcase/home.html', {"all_projects": all_projects,"all_users":all_users,'form':form,'comments':comments})

def project(request,project_id):
    if request.user.is_authenticated:
       user = User.objects.get(id=request.user.id)
       project = Project.objects.get(id = project_id)
       reviews = Review.objects.filter(project=project)
       design = reviews.aggregate(Avg('design'))['usability_avg']
       usability = reviews.aggregate(Avg('usability'))['usability_avg']
       content = reviews.aggregate(Avg('content'))['content_avg']
       average = reviews.aggregate(Avg('average'))['average_avg'] 
    if request.method == 'POST':
        form = VoteForm(request.POST)
        if form.is_valid:
            if project.userinterface == 1:
                project.userinterface = int(request.POST['userinterface'])
            else:
                project.userinterface = (project.userinterface + int(request.POST['userinterface']))/2
            if project.functionality == 1:
                project.functionality = int(request.POST['functionality'])
            else:
                project.functionality = (project.userinterface + int(request.POST['functionality']))/2
            if project.content == 1:
                project.content = int(request.POST['content'])
            else:
                project.content = (project.design + int(request.POST['content']))/2
    else:
        form = VoteForm()
    return render(request,'project.html',{'form':form,'project':project,'rating':rating})


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
    # uploader_profile = Project.objects.filter(projectuploader_profile=p).all()

    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.projectuploader_profile= p
            post.save()
            return redirect('/')
    else:
        form =PostForm()
    return render(request, 'showcase/upload.html', {"form": form})

@login_required(login_url='/accounts/login/')
def like(request, image_id):
    project = get_object_or_404(Project, pk=image_id)
    request.user.profile.like(project)
    return JsonReponse(project.count_likes, safe=False)

@login_required(login_url='/accounts/login/')
def unlike(request, project_id):
    image = get_object_or_404(Image, pk=post_id)
    request.user.profile.unlike(project)
    return JsonReponse(image.count_likes, safe=False)

    

def profile(request):
    return render(request,'showcase/profile.html')

def vote_project(request, project_id):
    project = Project.objects.get(id=project_id)
    rating = round(((project.userinterface + project.functionality)/2),2)
    if request.method == 'POST':
        form = VoteForm(request.POST)
        if form.is_valid:
            if project.userinterface == 1:
                project.userinterface = int(request.POST['userinterface'])
            else:
                project.userinterface = (project.userinterface + int(request.POST['userinterface']))/2
            if project.functionality == 1:
                project.functionality = int(request.POST['functionality'])
            else:
                project.functionality = (project.userinterface + int(request.POST['functionality']))/2
            if project.content == 1:
                project.content = int(request.POST['content'])
            else:
                project.content = (project.design + int(request.POST['content']))/2


