from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Client, ClubCard
import datetime

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('content:home')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

from datetime import date
from django.contrib import messages

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        birth_date_str = request.POST.get("birth_date")

        if birth_date_str:
            birth_date = date.fromisoformat(birth_date_str)

            today = date.today()

            age = (
                today.year
                - birth_date.year
                - (
                    (today.month, today.day)
                    < (birth_date.month, birth_date.day)
                )
            )

            if age < 18:
                messages.error(
                    request,
                    "Регистрация доступна только лицам старше 18 лет."
                )

                return render(
                    request,
                    "users/register.html",
                    {"form": form}
                )

        if form.is_valid():

            user = form.save()

            Client.objects.create(
                user=user,
                phone=request.POST.get("phone", ""),
                birth_date=birth_date
            )

            login(request, user)

            return redirect("content:home")

    else:
        form = UserCreationForm()

    return render(
        request,
        "users/register.html",
        {"form": form}
    )

def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect('content:home')

def set_currency_view(request):
    if request.method == "POST":
        currency = request.POST.get('currency', 'BYN')
        request.session['selected_currency'] = currency
    return redirect(request.META.get('HTTP_REFERER', 'content:home'))

@login_required
def profile_view(request):

    client = getattr(
        request.user,
        "client",
        None
    )

    cards = (
        ClubCard.objects.filter(client=client)
        if client
        else []
    )

    age = None

    if client and client.birth_date:

        today = datetime.date.today()

        age = (
            today.year
            - client.birth_date.year
            - (
                (today.month, today.day)
                <
                (
                    client.birth_date.month,
                    client.birth_date.day
                )
            )
        )

    return render(
        request,
        "users/profile.html",
        {
            "client": client,
            "cards": cards,
            "age": age
        }
    )

@login_required
def buy_card(request):
    if request.method == "POST":
        client = getattr(request.user, 'client', None)
        if client:
            card_type = request.POST.get('card_type', 'Standart')
            price = 500 if card_type == 'VIP' else 150
            ClubCard.objects.create(
                client=client,
                card_type=card_type,
                valid_to=datetime.date.today() + datetime.timedelta(days=30),
                price_paid=price
            )
    return redirect('users:profile')

def switch_role_view(request, role):
    from django.contrib.auth.models import User
    from django.contrib.auth import login
    if role == 'admin':
        u = User.objects.filter(username='admin').first()
        if u:
            login(request, u, backend='django.contrib.auth.backends.ModelBackend')
    elif role == 'instructor':
        u = User.objects.filter(username='trainer_ivan').first()
        if u:
            login(request, u, backend='django.contrib.auth.backends.ModelBackend')
    elif role == 'client':
        u = User.objects.filter(username='client_dmitry').first()
        if u:
            login(request, u, backend='django.contrib.auth.backends.ModelBackend')
    return redirect(request.META.get('HTTP_REFERER', 'content:home'))
