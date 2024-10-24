from django.shortcuts import render, redirect, get_object_or_404
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from .models import Review
from .forms import ReviewForm
from product.models import DrugEntry as Produk
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from .models import Produk, Review
from .forms import ReviewForm

def create_review(request, product_id=None):
    product = get_object_or_404(Produk, id=product_id) if product_id else None
    form = ReviewForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.product = product
        review.save()
        return redirect('reviews', product_id=product_id)
    context = { 'form': form, 'product': product }
    return render(request, 'create_review.html', context)

@csrf_exempt
@require_POST
def create_review_ajax(request, product_id=None):
    comment = strip_tags(request.POST.get("comment"))
    rating = request.POST.get("rating")
    product = get_object_or_404(Produk, id=product_id) if product_id else None
    review = Review(user=request.user, product=product, rating=rating, comment=comment)
    review.save()
    return HttpResponse(b"CREATED", status=201)

def edit_product(request, review_id):
    review = Review.objects.get(pk=review_id)
    form = ReviewForm(request.POST or None, instance = review)
    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('review:reviews'))
    return render(request, "edit_review.html", {'form': form, 'product': review.product })

def delete_review(request, review_id):
    Review.objects.get(pk=review_id).delete()
    return HttpResponseRedirect(reverse('review:reviews'))

def reviews(request, product_id=None):
    product = get_object_or_404(Produk, id=product_id) if product_id else None
    reviews = Review.objects.filter(product=product) if product else Review.objects.none()
    context = { 'product': product, 'reviews': reviews }
    return render(request, 'reviews_old.html', context)

def reviews_json(request, product_id=None):
    product = get_object_or_404(Produk, id=product_id) if product_id else None
    reviews = Review.objects.filter(product=product) if product else Review.objects.none()
    return HttpResponse(serializers.serialize("json", reviews), content_type="application/json")