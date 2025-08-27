from django.shortcuts import render , redirect ,HttpResponse
from .forms import MyUserCreationForm
from django.contrib.auth import login  , logout ,authenticate 
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from .models import MyUser , EmailOpt
import random
from django.core.mail import send_mail
from  django.conf import settings
from django.utils import timezone
from django.http import JsonResponse
import json
# Create your views here.
@login_required
def home(req):
  name = req.user.username
  return render(req , "home.html" , {"name" : name})


def request_otp_view(req):
  data = json.loads(req.body)
  email = data.get("email")
  req.session["sesion_email"] = email


 
  if req.method == "POST":
    if MyUser.objects.filter(email= email).exists():
     return JsonResponse({"message" :'Email aleardy exists'})
     
    otp = str(random.randint(100000, 999999))
    EmailOpt.objects.update_or_create(
      email = email ,
      defaults={"otp":otp,
                "created_at": timezone.now(),
                "opt_attempt" : 0},
      
    )
    send_mail(
      subject= 'Your otp code',
      message=f"your otp code is {otp} dont share it with anybody",
      from_email= settings.EMAIL_HOST_USER ,
      recipient_list=[email],
    )
    return JsonResponse({"message" : "OTP sent successfully!"})
  
  else :
    return JsonResponse({"message" : "Invalid request method"})
  
  

     
  



def signup_view(req) :
  if req.user.is_authenticated:   
        return redirect("home") 
  email = req.session.get("sesion_email" ,  "No email found")

  
  

  
  if req.method == "POST":
    if MyUser.objects.filter(email= email).exists():
     return JsonResponse({"error" : 'Email aleardy exists'})
    data = json.loads(req.body)


    form = MyUserCreationForm(data)
    otp_entered = data.get("otp")
    
    try :
      email_otp = EmailOpt.objects.get(email=email)
    except EmailOpt.DoesNotExist:
            return JsonResponse({"error" :"No OTP was sent to this email."})

    if email_otp.is_expired():
            return JsonResponse({"error":"OTP expired. Please request a new one."})

    if email_otp.can_attempt() :
      email_otp.opt_attempt += 1
      if email_otp.otp == otp_entered:
              if form.is_valid():
                user = form.save(commit=False)
                user.email = email
                user.save()
                login(req , user)
                email_otp.delete() 
                return JsonResponse({"address" : " "})
      else:
         email_otp.save()
         return JsonResponse({"error" : "wrong otp code" } )
      
    else:
            return JsonResponse({"error" : "failed request a new otp"})

    
  else :
    form = MyUserCreationForm()
    return render(req , 'signup.html' , {'form' : form})


def logout_view(req):
  logout(req)
  return redirect('login')


def login_view(req):
  if req.user.is_authenticated:
     return redirect('home')
  if req.method == "POST":
    form = LoginForm(req.POST)
    if form.is_valid() :
      username = form.cleaned_data["username"]
      password = form.cleaned_data["password"]

      user = authenticate(req , username = username , password = password)
      if user is not None:
        login(req , user)
        return redirect("home")
      else :
        return form.add_error(None ,"Invalid username or password")
  else :
    form = LoginForm()
    return render(req , "login.html" , {'form' : form})
