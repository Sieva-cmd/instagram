
import datetime as dt
from django.contrib.auth.decorators import login_required
from .models import Image,Profile,Preference,Comments,Follow
from django.http  import Http404,HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import  render, redirect,get_object_or_404
from .forms import NewUserForm,CommentForm,UpdateUserForm,UpdateUserProfileForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .email import send_welcome_email
from django.urls import reverse
from django.contrib.auth.models import User
    


# Create your views here.


def home(request):
    profile =Profile.objects.all()
    images =Image.filter_by_profile(profile)
    profiles =Profile.filter_profile_by_id(profile)
    return render(request,'main/home.html',{"images":images,"profiles":profiles})

def search_results(request):
    if 'image' in request.GET and request.GET["image"]:
        search_term =request.GET.get("image")
        searched_image =Image.search_image_by_name(search_term)
        message =f"{search_term}"

        return render(request,'main/search.html',{"message":message,"images":searched_image})
    else:
        message ="You haven't searched for an image"
        return render(request, 'main/search.html', {"message":message})    

@login_required(login_url='/login/')
def image(request,image_id):
    try:
        image = Image.objects.get(id = image_id)
    except ObjectDoesNotExist:
        raise Http404()
    return render(request,"main/image.html", {"image":image})



def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			send_welcome_email(user)
			messages.success(request, "Registration successful." )
			return redirect(login_request)
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="main/register.html", context={"register_form":form})


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect(home)
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request,template_name="main/login.html", context={"login_form":form})


def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect(login_request)    



@login_required(login_url='login')
def like(request, id):
    image = Image.objects.get(id = id)
    image.likes += 1
    image.save()
    return HttpResponseRedirect(reverse("home"))


@login_required(login_url='login')
def comment(request, id):
    image = Image.objects.get(id=id)
    comments = Comments.objects.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.image = image
            new_comment.user = request.user.profile
            new_comment.save()
            
            return HttpResponseRedirect(request.path_info)
            
    else:
        form = CommentForm()

    return render(request, 'main/post.html', {'image': image,'form': form,'comments':comments})

@login_required(login_url='login')
def profile(request, username):
    images = request.user.images.all()
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user.profile)
        profile_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(request.path_info)
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateUserProfileForm()

    return render(request, 'main/profile.html', {'user_form':user_form,'profile_form':profile_form,'images':images})


@login_required(login_url='login')
def user_profile(request, username):
    user_poster = get_object_or_404(User, username=username)
    if request.user == user_poster:
        return redirect('profile', username=request.user.username)
    user_posts = user_poster.images.all()
    
    followers = Follow.objects.filter(followed=user_poster.profile)
    if_follow = None
    for follower in followers:
        if request.user.profile == follower.follower:
            if_follow = True
        else:
            if_follow = False

    print(followers)
    return render(request, 'all-instagram/poster.html', {'user_poster': user_poster,'followers': followers, 'if_follow': if_follow,'user_posts':user_posts})
@login_required(login_url='login')
def unfollow(request, to_unfollow):
    if request.method == 'GET':
        unfollow_profile = Profile.objects.get(pk=to_unfollow)
        new_unfollowed = Follow.objects.filter(follower=request.user.profile, followed=unfollow_profile)
        new_unfollowed.delete()
        return redirect('user_profile', unfollow_profile.user.username)

@login_required(login_url='login')
def follow(request, to_follow):
    if request.method == 'GET':
        follow_profile = Profile.objects.get(pk=to_follow)
        new_following = Follow(follower=request.user.profile, followed=follow_profile)
        new_following.save()
        return redirect('user_profile', follow_profile.user.username)