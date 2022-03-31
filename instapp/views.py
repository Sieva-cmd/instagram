from django.shortcuts import render
import datetime as dt
from .models import Image,Profile
    


# Create your views here.


def home(request):
    profile =Profile.objects.all()
    images =Image.filter_by_profile(profile)
    return render(request,'main/home.html',{"images":images})
