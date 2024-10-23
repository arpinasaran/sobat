from django.shortcuts import render, redirect
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from .models import Review
from .forms import ReviewForm
from product.models import DrugEntry as Produk
from .models import Review
from django.http import HttpResponseRedirect
from django.urls import reverse

def create_review(request, product_id):
    product = Produk.objects.get(id=product_id)
    form = ReviewForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.product = product
        review.save()
        return redirect('product_reviews', product_id=product_id)
    context = {'form': form, 'product': product}
    return render(request, 'create_review.html', context)

@csrf_exempt
@require_POST
def create_review_ajax(request, product_id):
    comment = strip_tags(request.POST.get("comment"))
    rating = request.POST.get("rating")
    reviewer = request.user
    product = Produk.objects.get(id=product_id)
    review = Review(reviewer=reviewer, product=product, rating=rating, comment=comment)
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

def reviews(request, product_id):
    product = Produk.objects.get(id=product_id)
    reviews = Review.objects.filter(product=product)
    context = {'product': product, 'reviews': reviews }
    return render(request, 'reviews.html', context)