from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from authentication.forms import CreateUserForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from authentication.models import User
import json

# Create your views here.
def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('authentication:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
   if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.error(request, "Invalid username or password. Please try again.")
   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('authentication:login'))
    response.delete_cookie('last_login')
    return response

@csrf_exempt
def register_mobile(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        nama = data['nama']
        username = data['username']
        password1 = data['password1']
        password2 = data['password2']
        role = data['role']

        # Check if the passwords match
        if password1 != password2:
            return JsonResponse({
                "status": False,
                "message": "Passwords do not match."
            }, status=400)
        
        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "status": False,
                "message": "Username already exists."
            }, status=400)
        
        # Create the new user
        user = User.objects.create_user(nama=nama, username=username, password=password1, role=role)
        user.save()
        
        return JsonResponse({
            "username": user.username,
            "status": 'success',
            "message": "User created successfully!"
        }, status=200)
    
    else:
        return JsonResponse({
            "status": False,
            "message": "Invalid request method."
        }, status=400)

@csrf_exempt
def login_mobile(request):
    nama = request.POST['nama']
    username = request.POST['username']
    password = request.POST['password']
    role = request.POST['role']
    
    # Autentikasi pengguna
    user = authenticate(nama=nama, username=username, password=password, role=role)
    
    if user is not None:
        if user.is_active:
            login(request, user)
            # Status login sukses, termasuk user_id
            return JsonResponse({
                "user_id": user.id,  # Menambahkan user_id dalam response
                "nama": user.nama,
                "username": user.username,
                "role": user.role,
                "status": True,
                "message": "Login sukses!"
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login gagal, akun dinonaktifkan."
            }, status=401)

    else:
        return JsonResponse({
            "status": False,
            "message": "Login gagal, periksa kembali email atau kata sandi."
        }, status=401)

@csrf_exempt
def logout_mobile(request):
    username = request.user.username

    try:
        logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logout berhasil!"
        }, status=200)
    except:
        return JsonResponse({
        "status": False,
        "message": "Logout gagal."
        }, status=401)
    
@csrf_exempt
def get_user_role(request):
    try:
        print("User authenticated:", request.user.is_authenticated)  # Debug print
        print("User:", request.user)  # Debug print
        if request.user.is_authenticated:
            print("User role:", request.user.role)  # Debug print
            return JsonResponse({
                'status': 'success',
                'role': request.user.role,
                'message': 'Role retrieved successfully'
            })
        return JsonResponse({
            'status': 'error',
            'role': '',
            'message': 'User not authenticated'
        })
    except Exception as e:
        print("Error in get_user_role:", str(e))  # Debug print
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })