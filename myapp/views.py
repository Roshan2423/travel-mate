# views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from myapp.forms import CustomSignupForm  # Ensure this import is correct
from myapp.models import QuestionAnswer
import json
import requests

# Groq API key
GROQ_API_KEY = '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'
GROQ_API_URL = 'https://console.groq.com/v1/query'

def index(request):
    return render(request, 'myapp/index.html')

def login_view(request):
    return render(request, 'myapp/login.html')

def signup_view(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            form.save(request)
            return redirect('account_login')
    else:
        form = CustomSignupForm()
    return render(request, 'myapp/signup.html', {'form': form})

@csrf_exempt
def chatbot(request):
    if request.method == 'POST':
        try:
            body_unicode = request.body.decode('utf-8')
            data = json.loads(body_unicode)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON format'}, status=400)

        user_message = data.get('message', '')

        # Check for predefined questions
        predefined_answer = get_predefined_answer(user_message)
        if predefined_answer:
            return JsonResponse({'message': predefined_answer})

        # If no predefined answer, query Groq API
        groq_answer = query_groq_api(user_message)
        return JsonResponse({'message': groq_answer})

    return JsonResponse({'message': 'Invalid request method.'}, status=400)

def get_predefined_answer(user_message):
    try:
        question_answer = QuestionAnswer.objects.get(question__iexact=user_message)
        return question_answer.answer
    except QuestionAnswer.DoesNotExist:
        return None

def query_groq_api(user_message):
    headers = {
        'Authorization': f'Bearer {GROQ_API_KEY}',
        'Content-Type': 'application/json',
    }
    payload = {
        'query': user_message,
    }
    response = requests.post(GROQ_API_URL, headers=headers, json=payload)
    groq_response = response.json()

    if 'error' in groq_response:
        return 'Sorry, I cannot answer that right now.'

    return groq_response.get('response', 'Sorry, I cannot answer that right now.')
