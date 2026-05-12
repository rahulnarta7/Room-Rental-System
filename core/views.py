from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404,redirect
from .models import Room
from .forms import RoomForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib import messages

def login_view(request):

    if request.method == "POST":

        username_or_email = request.POST.get("username")
        password = request.POST.get("password")

        user = None

        
        user = authenticate(
            request,
            username=username_or_email,
            password=password
        )

       
        if user is None:

            users = User.objects.filter(email=username_or_email)

            if users.exists():

                
                user_obj = users.first()

                user = authenticate(
                    request,
                    username=user_obj.username,
                    password=password
                )

        
        if user is not None:

            login(request, user)
            return redirect('home')

        else:
            messages.error(request, "Invalid username/email or password")

    return render(request, "login.html")

def home(request):
    rooms = Room.objects.all()

    location = request.GET.get('location')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if location or min_price or max_price:
        if location:
            rooms = rooms.filter(location__icontains=location)

        if min_price:
            rooms = rooms.filter(price__gte=min_price)

        if max_price:
            rooms = rooms.filter(price__lte=max_price)

        top_rooms = rooms   
    else:
        top_rooms = Room.objects.all()[:3] 

    context = {
        'top_rooms': top_rooms,
        'location': location,
        'min_price': min_price,
        'max_price': max_price
    }

    return render(request, 'home.html', context)

def all_rooms(request):
    rooms = Room.objects.all()

    return render(request, "all_rooms.html", {
        "rooms": rooms
    })
def room_detail(request, id):
    room = get_object_or_404(Room, id=id)
    return render(request, 'room_detail.html', {'room': room})


@login_required
def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)

        if form.is_valid():
            room = form.save(commit=False)
            room.owner = request.user
            room.save()
            return redirect('home')
    else:
        form = RoomForm()

    return render(request, 'add_room.html', {'form': form})
    
@login_required
def edit_room(request, id):
    room = get_object_or_404(Room, id=id)

   
    if room.owner != request.user:
        return redirect('home')   # or HttpResponseForbidden()

    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RoomForm(instance=room)

    return render(request, 'add_room.html', {'form': form})

@login_required
def delete_room(request, id):
    room = get_object_or_404(Room, id=id)

    if room.owner != request.user:
        return redirect('home')

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'confirm_delete.html', {'room': room})

#user register
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

def register(request):

    if request.method == 'POST':

        username = request.POST.get('username').strip()
        email = request.POST.get('email').strip().lower()
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Password match check
        if password1 != password2:

            return render(request, 'register.html', {
                'error': 'Passwords do not match'
            })

        # Username exists
        if User.objects.filter(username=username).exists():

            return render(request, 'register.html', {
                'error': 'Username already exists'
            })

        # Email exists
        if User.objects.filter(email=email).exists():

            return render(request, 'register.html', {
                'error': 'Email already exists'
            })

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        user.save()

        messages.success(request, "Account created successfully")

        return redirect('/accounts/login/')

    return render(request, 'register.html')

@login_required
def my_listings(request):
    rooms = Room.objects.filter(owner=request.user)
    return render(request, 'my_listings.html', {'rooms': rooms})
