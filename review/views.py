from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReviewForm
from product.models import DrugEntry as Produk
from authentication.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .models import Produk, Review
from django.db.models import Avg

def create_review(request, product_id=None):
    product = get_object_or_404(Produk, id=product_id) if product_id else None
    form = ReviewForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.product = product
        review.save()
        return redirect('review:reviews', product_id=product_id)
    context = { 'form': form, 'product': product }
    return render(request, 'create_review.html', context)

def edit_review(request, review_id, product_id):
    review = Review.objects.get(pk=review_id)
    form = ReviewForm(request.POST or None, instance = review)
    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('review:reviews', args=[product_id]))
    return render(request, "edit_review.html", {'form': form, 'product': review.product })

def delete_review(request, review_id, product_id):
    Review.objects.get(pk=review_id).delete()
    return HttpResponseRedirect(reverse('review:reviews', args=[product_id]))

def reviews(request, product_id=None):
    product = get_object_or_404(Produk, id=product_id) if product_id else None
    all_reviews = Review.objects.filter(product=product) if product else Review.objects.none()
    
    selected_rating = request.GET.get('rating')
    search_query = request.GET.get('search', '')

    if product:
        reviews = Review.objects.filter(product=product)
        
        if selected_rating:
            reviews = reviews.filter(rating=selected_rating)
        
        if search_query:
            reviews = [
                review for review in reviews 
                if search_query.lower() in review.user.nama.lower() or search_query.lower() in review.comment.lower()
            ]
    else:
        reviews = Review.objects.none()

    average_rating = all_reviews.aggregate(Avg('rating'))['rating__avg'] if all_reviews.exists() else None
    if average_rating is not None:
        average_rating = round(average_rating, 1)

    context = {
        'product': product,
        'reviews': reviews,
        'average_rating': average_rating,
        'search_query': search_query
    }
    return render(request, 'reviews.html', context)


def reviews_json(request, product_id):
    product = get_object_or_404(Produk, id=product_id)
    reviews = Review.objects.filter(product=product)
    reviews_data = [
        {
            "id": review.id,
            "user": review.user.id,
            "username": review.user.nama,
            "product": review.product.id,
            "rating": review.rating,
            "comment": review.comment,
            "date_created": review.date_created,
        }
        for review in reviews
    ]
    return JsonResponse(reviews_data, safe=False)