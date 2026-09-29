from django.shortcuts import render,redirect
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import SignupForm
from .models import UserProfile

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import RegisterSerializer, LoginSerializer


# Create your views here.

def signup(request):
    if request.user.is_authenticated:
        return redirect("book:home")
    form = SignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.email = form.cleaned_data["email"]
        user.first_name = form.cleaned_data["username"]
        user.save()
        UserProfile.objects.create(
            user=user,
            address=form.cleaned_data["address"],
            phone_number=form.cleaned_data["phone_number"],
        )
        login(request, user)
        messages.success(request, "Account created successfully.")
        return redirect("book:home")
    return render(request, "signup.html", {"form": form})



def login_view(request):
    if request.user.is_authenticated:
        return redirect("book:home")
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, "Logged in successfully.")
        return redirect("book:home")
    return render(request, "login.html", {"form": form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("book:home")

@login_required
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, "profile.html", {"user_profile": user_profile})




class RegisterAPIView(ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = RegisterSerializer

class LoginAPIView(RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = LoginSerializer


    