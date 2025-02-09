import json
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReviewForm
from product.models import DrugEntry as Produk
from authentication.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .models import Review
from django.db.models import Avg
from django.views.decorators.csrf import csrf_exempt

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

@csrf_exempt
def create_review_flutter(request, product_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product = Produk.objects.get(id=product_id)
            new_review = Review.objects.create(
                user=request.user,
                product=product,
                rating=int(data["rating"]),
                comment=data["comment"]
            )
            new_review.save()
            return JsonResponse({"status": "success"}, status=200)
        except Produk.DoesNotExist:
            return JsonResponse({"status": "error"}, status=404)
        except Exception:
            return JsonResponse({"status": "error"}, status=400)
    else:
        return JsonResponse({"status": "error"}, status=405)

@csrf_exempt
def edit_review_flutter(request, review_id, product_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            review = Review.objects.get(id=review_id)
            review.rating = int(data["rating"])
            review.comment = data["comment"]
            review.save()

            return JsonResponse({"status": "success"}, status=200)
        except Review.DoesNotExist:
            return JsonResponse({"status": "error"}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error"}, status=400)
    else:
        return JsonResponse({"status": "error"}, status=405)

@csrf_exempt
def delete_review_flutter(request, review_id, product_id):
    if request.method == 'POST':
        try:
            review = Review.objects.get(id=review_id)
            review.delete()
            return JsonResponse({"status": "success"}, status=200)
        except Review.DoesNotExist:
            return JsonResponse({"status": "error"}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error"}, status=400)
    else:
        return JsonResponse({"status": "error"}, status=405)