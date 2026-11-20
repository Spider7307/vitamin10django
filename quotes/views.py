from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Quote
import random
import json

# ============ TEMPLATE VIEWS (return HTML) ============

# TODO 7: Create a home view
#   - Get all quotes from database: Quote.objects.all()
#   - Pick a random quote
#   - Render 'quotes/home.html' with quote in context
def home(request):
    quotes = Quote.objects.all()
    quote = random.choice(list(quotes)) if quotes else None
    return render(request,'quotes/home.html',{'quote':quote})

# TODO 8: Create an all_quotes view
#   - Get all quotes
#   - Render 'quotes/all_quotes.html' with quotes in context
def all_quotes(request):
    quotes=Quote.objects.all()
    return render(request,'quotes/all_quotes.html',{'quotes':quotes})


# ============ API VIEWS (return JSON) ============

# TODO 9: Create a random_quote_api view
#   - Get all quotes, pick random one
#   - Return JsonResponse with 'id', 'text', 'author'
def random_quote_api(request):
    quotes = Quote.objects.all()
    quote = random.choice(list(quotes)) if quotes else None
    if not quote:
        return JsonResponse({'error':'No quotes found'},status=404)
    return JsonResponse({'id':quote.id,'text':quote.text,'author':quote.author})

@csrf_exempt  # Allows POST/PUT/DELETE without CSRF token
def quotes_api(request):
    # TODO 10: Handle GET and POST for /api/quotes/
    #   GET: Return all quotes as JSON (use safe=False for lists)
    #   POST: Create new quote from request.body, return with status 201
    #   Check request.method to determine which action
    if request.method=='GET':
        quotes=Quote.objects.all()
        data =[{'id':q.id,'text':q.text,'author':q.author} for q in quotes]
        return JsonResponse(data,safe=False)
    elif request.method=='POST':
        try:
            data=json.loads(request.body)
            quote=Quote.objects.create(text=data['text'],author=data['author'])
            return JsonResponse({'id':quote.id,'text':quote.text,'author':quote.author},status=201)
        except (json.JSONDecodeError,KeyError,TypeError):
            return JsonResponse({'error':'Invalid quote data'},status=400)
    return JsonResponse({'error':'Method not allowed'},status=405)


@csrf_exempt
def quote_detail_api(request, id):
    # TODO 11: Handle GET, PUT, DELETE for /api/quotes/<id>/
    #   GET: Return single quote as JSON (404 if not found)
    #   PUT: Update quote from request.body, return updated quote
    #   DELETE: Delete quote, return success message
    #   Check request.method to determine which action
    quote = Quote.objects.get(id=id)
    if request.method=='GET':
        return JsonResponse({'id':quote.id,'text':quote.text,'author':quote.author})
    elif request.method=='PUT':
        try:
            data=json.loads(request.body)
            quote.text=data.get('text', quote.text)
            quote.author=data.get('author', quote.author)
            quote.save()
            return JsonResponse({'id':quote.id,'text':quote.text,'author':quote.author})
        except (json.JSONDecodeError, TypeError):
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    elif request.method == 'DELETE':
        quote.delete()
        return JsonResponse({'message': 'Quote deleted successfully'})
    return JsonResponse({'error': 'Method not allowed'}, status=405)