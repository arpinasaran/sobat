from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReviewForm
from product.models import DrugEntry as Produk
from authentication.models import User
from django.http import HttpResponseRedirect
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
    users = User.objects.filter(role='pengguna')
    all_reviews = Review.objects.filter(product=product) if product else Review.objects.none()
    selected_user_id = request.GET.get('user')
    if product:
        if selected_user_id:
            reviews = Review.objects.filter(product=product, user_id=selected_user_id)
        else:
            reviews = Review.objects.filter(product=product)
    else:
        reviews = Review.objects.none()

    average_rating = all_reviews.aggregate(Avg('rating'))['rating__avg'] if all_reviews.exists() else None
    if average_rating is not None:
        average_rating = round(average_rating, 1)

    context = { 'product': product, 'reviews': reviews, 'users': users, 'average_rating': average_rating }
    return render(request, 'reviews.html', context)