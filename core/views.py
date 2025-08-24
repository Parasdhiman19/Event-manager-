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
# Create your views here.
@login_required
def home(req):
  return render(req , "home.html")


def request_otp_view(req):
  if req.method == "POST":
    email = req.POST.get("email")
    otp = str(random.randint(100000, 999999))
    EmailOpt.objects.update_or_create(
      email = email ,
      defaults={"otp":otp,
                "created_at": timezone.now()}
      ,
      
    )
    req.session["email"] = email
    send_mail(
      subject= 'Your otp code',
      message=f"your otp code is {otp} dont share it with anybody",
      from_email= settings.EMAIL_HOST_USER ,
      recipient_list=[email],
    )
    return JsonResponse("OTP sent successfully!")
  
  else :
    return JsonResponse("Account aleaready exists login!")
  
  

     
  



def signup_view(req) :
  if req.method == "POST":

    form = MyUserCreationForm(req.POST)
    email = req.POST.get("email")
    otp_entered = req.POST.get("otp")
    try :
      email_otp = EmailOpt.objects.get(email=email)
    except EmailOpt.DoesNotExist:
            return HttpResponse("No OTP was sent to this email.")

    if email_otp.is_expired():
            return HttpResponse("OTP expired. Please request a new one.")

        # 2. Check OTP match
    if email_otp.otp == otp_entered:
            if form.is_valid():
              user = form.save()
              login(req , user)
              
            # ✅ OTP correct
            # (Here you can create the user or allow signup)
              email_otp.delete()  # optional: remove OTP after success
              return redirect("home")
    else:
            return HttpResponse("Invalid OTP. Try again.")

    
  else :
    form = MyUserCreationForm()
    return render(req , 'signup.html' , {'form' : form})


def logout_view(req):
  logout(req)
  return redirect('login')


def login_view(req):
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
