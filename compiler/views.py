from http.client import HTTPResponse
from importlib.util import source_hash

from django.db.models.expressions import result
from django.shortcuts import render,redirect
from pyexpat.errors import messages
import ast
from .forms import RegisterForm,LoginForm
from .models import User, CodingChallenge
import requests
from django.http import JsonResponse
import csv
import os
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse
from django.db.models import Sum,Count
from .models import CodingChallenge,Submission,DIFFICULTY_POINTS
from .forms import SubmissionForm


#homepage
def home(request):
    return render(request,'main.html')

#python basics page
def python_basics(request):
    return render(request,'pythonbasics.html')
def c_basics(request):
    return render(request,'cbasics.html')
def cpp_basics(request):
    return render(request,'c++basics.html')
def java_basics(request):
    return render(request,'javabasics.html')

#sign in
def signin(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(username=uname,email=email)
                return redirect('main')
            except User.DoesNotExist:
                return render(request,'signin.html',{'form':form,'error':'Invalid username or email'})
    else:
        form = LoginForm()
    return render(request,'signin.html',{'form':form})

#register
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signin')
        else:
            form = RegisterForm()
        return render(request,'register.html',{'form':form})

#codecompiler
import requests
from django.http import JsonResponse
from django.shortcuts import render

def codecompiler(request):
    output = ""
    if request.method == "POST":
        code = request.POST.get('code')
        language = request.POST.get('language')

        # Judge0 language mapping
        lang_map = {
            'python': 71,
            'c++': 54,
            'java': 62,
            'c': 50
        }

        url = "https://judge0-ce.p.rapidapi.com/submissions?base64_encoded=false&wait=true"

        payload = {
            'source_code': code,
            'language_id': lang_map.get(language.lower(), 71),
            'stdin': ''
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-RapidAPI-Host': 'judge0-ce.p.rapidapi.com',
            'X-RapidAPI-Key': '42aec8e3c2msh9cc11a60394612dp1a5cc8jsnea571e546629'  # replace with your key
        }

        try:
            response = requests.post(url, data=payload, headers=headers)
            result = response.json()

            # Extract output correctly
            output = result.get('stdout')
            if output is None:
                output = result.get('compile_output') or result.get('stderr') or "No output"

        except Exception as e:
            output = f"Error parsing output: {e}"

        return JsonResponse({'output': output})

    return render(request, 'compiler.html')

from django.shortcuts import render

#AI chatbot

from django.shortcuts import render
import google.generativeai as genai
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
import requests
from django.conf import settings

OPENROUTER_API_KEY = getattr(settings, "OPENROUTER_API_KEY", "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")

def aichatbot(request):
    if request.method == "POST":
        prompt = request.POST.get("message")
        if not prompt:
            return JsonResponse({"error": "No message provided."})
        try:
            url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            }
            data = {
                "model": "meta-llama/llama-3-8b-instruct",
                "messages":[
                    {"role":"system","content":"You are an AI tutor."},
                    {"role":"user","content": prompt}
                ],
            }
            response = requests.post(url, headers=headers, json=data)
            reply = response.json()["choices"][0]["message"]["content"]
            return JsonResponse({"reply": reply.strip()})
        except Exception as e:
            return JsonResponse({"error": str(e)})

    # GET request
    return render(request, "aichatbot.html")