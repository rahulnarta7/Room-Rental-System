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

        # Check if input is email
        if "@" in username_or_email:
            try:
                user_obj = User.objects.get(email=username_or_email)
                username = user_obj.username
            except User.DoesNotExist:
                username = None
        else:
            username = username_or_email

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")

    return render(request, "login.html")

def home(request):
    # rooms = Room.objects.filter(is_available=True)
    rooms = Room.objects.all()

    location = request.GET.get('location')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if location:
        rooms = rooms.filter(location__icontains=location)

    if min_price:
        rooms = rooms.filter(price__gte=min_price)

    if max_price:
        rooms = rooms.filter(price__lte=max_price)
    context = {
        'rooms': rooms,
        'location': location,
        'min_price': min_price,
        'max_price': max_price
    }
    return render(request, 'home.html', context)

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
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # ✅ Check passwords match
        if password1 != password2:
            return render(request, 'register.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username exists'})

        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email exists'})

        # ✅ Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        user.save()

        return redirect('/accounts/login/')

    return render(request, 'register.html')

@login_required
def my_listings(request):
    rooms = Room.objects.filter(owner=request.user)
    return render(request, 'my_listings.html', {'rooms': rooms})
