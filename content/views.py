from io import BytesIO

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator

from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required

from users.models import Client, Instructor
from reviews.models import Review

from .models import (
    News,
    GlossaryTerm,
    Vacancy,
    FAQ,
    CompanyHistory,
    CompanyContact
)

from .forms import GlossaryTermForm

@user_passes_test(lambda u: u.is_superuser)
def term_create(request):

    if request.method == "POST":
        form = GlossaryTermForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('content:term_list')

    else:
        form = GlossaryTermForm()

    return render(
        request,
        'content/term_form.html',
        {'form': form}
    )

@user_passes_test(lambda u: u.is_superuser)
def term_edit(request, pk):

    term = get_object_or_404(
        GlossaryTerm,
        pk=pk
    )

    if request.method == "POST":
        form = GlossaryTermForm(
            request.POST,
            instance=term
        )

        if form.is_valid():
            form.save()
            return redirect('content:term_list')

    else:
        form = GlossaryTermForm(instance=term)

    return render(
        request,
        'content/term_form.html',
        {'form': form}
    )

@user_passes_test(lambda u: u.is_superuser)
def term_delete(request, pk):

    term = get_object_or_404(
        GlossaryTerm,
        pk=pk
    )

    term.delete()

    return redirect('content:term_list')

def home_view(request):
    latest_news = News.objects.order_by('-published_date')[:1]
    return render(request, 'content/home.html', {'latest_news': latest_news})

def about_view(request):
    history = CompanyHistory.objects.all().order_by("year")
    contacts = CompanyContact.objects.all()
    return render(request, "content/about.html", {
        "history": history,
        "contacts": contacts
    })

def news_list(request):
    news_list = News.objects.all().order_by('-published_date')
    paginator = Paginator(news_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'content/news_list.html', {'news': page_obj})

def news_detail(request, slug):
    item = get_object_or_404(News, slug=slug)
    return render(request, 'content/news_detail.html', {'item': item})

def term_list(request):
    terms_list = GlossaryTerm.objects.all().order_by('term')
    paginator = Paginator(terms_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'content/term_list.html', {'terms': page_obj})

def vacancies(request):
    vacs = Vacancy.objects.filter(is_active=True)
    return render(request, 'content/vacancies.html', {'vacancies': vacs})

def faq_view(request):
    faqs = FAQ.objects.all()
    return render(request, 'content/faq.html', {'faqs': faqs})

def contacts_view(request):
    contacts = CompanyContact.objects.all()
    return render(request, 'content/contacts.html', {
        'contacts': contacts
    })

def privacy_view(request):
    return render(request, 'content/privacy.html')

@staff_member_required
def statistics_page(request):
    return render(
        request,
        "content/statistics.html"
    )


@staff_member_required
def statistics_chart(request):

    labels = [
        "Клиенты",
        "Инструкторы",
        "Отзывы",
        "Термины"
    ]

    values = [
        Client.objects.count(),
        Instructor.objects.count(),
        Review.objects.count(),
        GlossaryTerm.objects.count()
    ]

    plt.figure(figsize=(8, 5))
    plt.bar(labels, values)

    plt.title("Статистика клуба ФОРСАЖ")
    plt.ylabel("Количество")

    buffer = BytesIO()

    plt.savefig(
        buffer,
        format="png",
        bbox_inches="tight"
    )

    plt.close()

    buffer.seek(0)

    return HttpResponse(
        buffer.getvalue(),
        content_type="image/png"
    )