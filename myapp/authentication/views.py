from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout


def home(request):
    return render(request, "authentication/index.html")


def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        passwordConfirm = request.POST.get("confirm-pass")

        formData = {
            "username": username or "",
            "fname": fname or "",
            "lname": lname or "",
            "email": email or "",
        }
        print(formData)
        # validation start
        if User.objects.filter(username=username):
            messages.error(request, "Username already exists!")
            return render(request, "authentication/signup.html", formData)
        if User.objects.filter(email=email):
            messages.error(request, "Email already exists")
            return render(request, "authentication/signup.html", formData)
        if len(username) > 10 or len(username) < 4:
            messages.error(request, "Username must be between 4-10 characters")
            return render(request, "authentication/signup.html", formData)

        if password != passwordConfirm:
            messages.error(request, "Password don't match")
            return render(request, "authentication/signup.html", formData)
        if not username.isalnum():
            messages.error(request, "Username must be alphanumeric")
            return render(request, "authentication/signup.html", formData)
        # validation end

        myUser = User.objects.create_user(username, email, password)
        myUser.first_name = fname
        myUser.last_name = lname
        myUser.save()

        messages.success(request, "Your account has been successfully created.")

        return redirect("signin")

    return render(request, "authentication/signup.html")


def signin(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "authentication/index.html", {"fname": fname})
        else:
            messages.error(request, "Bad Credentials")
            return render(request, "authentication/signin.html", {"username": username})

    return render(request, "authentication/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "logged out successfully")
    return redirect("home")
