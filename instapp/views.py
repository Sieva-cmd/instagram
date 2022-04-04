from django.shortcuts import render
import datetime as dt
from .models import Image,Profile
    


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