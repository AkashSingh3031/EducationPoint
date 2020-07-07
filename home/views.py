from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from blog.models import Post
import requests
import json

# Create your views here.
def home(request):
    return render(request, 'home/home.html')

def about(request):
    return render(request, 'home/about.html')

def contact(request):
    if request.method=='POST':
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        content = request.POST['content']
        # print(name, phone, email, content)

        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, "Please fill the form correctly!\n Length --> Name > 2, Email > 3, Phone > 10, Comment > 4")
        else:
            contact = Contact(name=name, phone=phone, email=email, content=content)
            contact.save()
            messages.success(request, "Your message has been successfully sent!")

        #reCAPTCHA Stuff
        clientKey = request.POST("g-recaptcha-response")
        secretKey = '6LeSpaMZAAAAADdgnXmrQXWqg2ZUWGOm8LJJBaPl'
        captchaData = {
            'secret':secretKey,
            'response':clientKey
        }
        r = request.POST("https://www.google.com/recaptcha/api/siteverify", data=captchaData)
        response = json.loads(r.text)
        verify = response['success']
        if verify:
            return HttpResponse('<script> alert("success");</script>')
        else:
            return HttpResponse('<script> alert(" Not success");</script>')

    return render(request, 'home/contact.html')

def search(request):
    query = request.GET['query']
    if len(query)>50: 
        allPosts  = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)
    
    if allPosts.count() == 0:
        messages.warning(request, "No search results found. Please refine your query")
    params = {'allPosts':allPosts, 'query':query}
    return render(request, 'home/search.html', params)


def handleSignup(request):
    if request.method == 'POST':
        # Get the post parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Chech error 
        if len(username) > 15:
            messages.error(request, "Username must be under 15 characters")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, "Username should only contain letters and numbers")
            return redirect('home')

        if pass1 != pass2:
            messages.error(request, "Password do not match")
            return redirect('home')


        # create user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your account has been successfully created")
        return redirect('home')
    
    else:
        messages.error(request, "Your account has not been submit.")
        return HttpResponse('404 - Not Found')


def handleLogin(request):
    if request.method == 'POST':
        # Get the post parameters
        lofinusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']

        user = authenticate(username=lofinusername, password=loginpass)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials, Please try again...")
            return redirect('home')
        
    return HttpResponse('404 - Not Found')

def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('home')
    

