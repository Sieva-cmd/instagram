
import datetime as dt
from django.contrib.auth.decorators import login_required
from .models import Image,Profile
from django.http  import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
    


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
			# login(request, user)
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