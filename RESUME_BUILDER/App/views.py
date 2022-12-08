from email import message
import email
from http import client
from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponseNotFound
from faunadb import query as q
import pytz
from faunadb.objects import Ref
from faunadb.client import FaunaClient
import hashlib
import datetime

from requests import request

# Create your views here.


client = FaunaClient(secret="fnAE0ApimmACSzzzk_XzFVyppkYuEf_5UM6ZdUxb")
indexes = client.query(q.paginate(q.indexes()))


#Index Page
def index(request):
    return render(request,"index.html")



#Login Functionality

def login(request):
    if request.method == "POST":
        username = request.POST.get("username").strip().lower()
        password = request.POST.get("password")
        
        try:
            user =  client.query(q.get(q.match(q.index("users_index"),username)))
            if hashlib.sha512(password.encode()).hexdigest() == user[data][password]:
                request.session["user"] = {
                    "id": user["ref"].id(),
                    "username":user["data"]["username"]
                }
                return redirect("App:index")
            else:
                raise Exception()
        except Exception:
            message.add_message(request,message.INFO, " Wrong Credentials, Please try again!","danger")
            return redirect("App:login")
        
    return render(request,"login.html")


#Register Functionality

def register(request):
    if request.method == "POST":
        username = request.POST.get("username").strip().lower()
        email = request.POST.get("email").strip().lower()
        password = request.get("password")
        
        try:
            if(client.query(q.get(q.match(q.index("users_index"),username)))):
                message.add_message(request,message.INFO,"User already exist with that username")
            elif(client.query(q.get(q.match(q.index("users_index"),email)))):
                message.add_message(request,message.INFO,"User already exist with that email")
            return redirect("App:register")
        except:
            user = client.query(q.create(q.collection("Users"),{
                "data":{
                    "username":username,
                    "email":email,
                    "password": hashlib.sha512(password.encode()).hexdigest(),
                    "date":datetime.datetime.now(pytz.UTC)
                }
            }))
            message.add_message(request,message.INFO,"Registeration Successfull.")
            return redirect("App: login")
    return render(request,"register.html")

#Create-Resume Functionality

def create_resume:
    
    if request.method == "POST":
        username = request.session["user"]["username"]
        full_name = request.POST.get("name")
        address=request.POST.get("address")
        phone=request.POST.get("phone")
        email=request.POST.get("email")
        about_you=request.POST.get("about")
        education=request.POST.get("education")
        career=request.POST.get("career")
        job_1__start=request.POST.get("job-1__start")
        job_1__end=request.POST.get("job-1__end")
        job_1__details=request.POST.get("job-1__details")
        job_2__start=request.POST.get("job-2__start")
        job_2__end=request.POST.get("job-2__end")
        job_2__details=request.POST.get("job-2__details")
        job_3__start=request.POST.get("job-3__start")
        job_3__end=request.POST.get("job-3__end")
        job_3__details=request.POST.get("job-3__details")
        references=request.POST.get("references")
        
        try:
            resume = client.query(q.get(q.match(q.index("resume_index"),username)))
            resume_data = client.query(q.update(q.ref(q.collection("resume_info"),resume["ref"].id()),{
                "data":{
                    "user":username,
                    "full_name":full_name,
                    "address":address,
                    "phone":phone,
                    "email":email,
                    "about_you":about_you,
                    "education":education,
                    "career":career,
                    "job_1__start":job_1__start,
                    "job_1__end":job_1__end,
                    "job_1__details":job_1__details,
                    "job_2__start":job_2__start,
                    "job_2__end":job_2__end,
                    "job_2__details":job_2__details,
                    "job_3__start":job_3__start,
                    "job_3__end":job_3__end,
                    "job_3__details":job_3__details,
                    "references":references
                }
            }))
            messages.add_message(request,messages.INFO,'Resume Info Edited Successfully. Download Resume Now')
            return redirect("App:create-resume")
        except:
            resume_data = client.query(q.create(q.collection("resume_info"),{
                "data":{
                    "user":username,
                    "full_name":full_name,
                    "address":address,
                    "phone":phone,
                    "email":email,
                    "about_you":about_you,
                    "education":education,
                    "career":career,
                    "job_1__start":job_1__start,
                    "job_1__end":job_1__end,
                    "job_1__details":job_1__details,
                    "job_2__start":job_2__start,
                    "job_2__end":job_2__end,
                    "job_2__details":job_2__details,
                    "job_3__start":job_3__start,
                    "job_3__end":job_3__end,
                    "job_3__details":job_3__details,
                    "references":references
                }
            }))
            messages.add_message(request,messages.INFO,'Resume Info Edited Successfully. Download Resume Now')
            return redirect("App:resume")
    else:
        try:
            