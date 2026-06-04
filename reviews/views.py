from django.shortcuts import render, redirect
from .models import Review
from users.models import Client
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

def review_list(request):
    reviews_list = Review.objects.filter(is_approved=True).order_by('-created_at')
    paginator = Paginator(reviews_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'reviews/list.html', {'reviews': page_obj})

@login_required
def add_review(request):
    if request.method == "POST":
        client = getattr(request.user, 'client', None)
        if not client:
            messages.error(request, 'Только клиенты могут оставлять отзывы!')
            return redirect('reviews:list')
            
        rating = int(request.POST.get('rating', 5))
        comment = request.POST.get('comment')
        
        Review.objects.create(
            client=client,
            rating=rating,
            comment=comment,
            is_approved=True
        )
        messages.success(request, 'Спасибо! Ваш отзыв опубликован.')
    return redirect('reviews:list')
