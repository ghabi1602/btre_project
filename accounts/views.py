from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact

def register(request):

    if request.method == "POST":
        #Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        #password validation
        if password == password2:
            #check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'username is being taken already')
                return redirect('register')
                #check email
            
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'email is being used already')
                return redirect('register')
            else:
                #looks good
                user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password
                )
                user.save()
                messages.success(request, 'you have successfully registered')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')


def login(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(
            username=username,
            password=password
            )
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Logged in Successfully')
            return redirect('dashboard')
        else:
            messages.error(request, 'Login Failed')
            return redirect('login')
    return render(request, 'accounts/login.html')


def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)

    context = {
        'contacts': user_contacts
    }
    return render(request, 'accounts/dashboard.html', context)


def logout(request):
    if request.method == "POST":
        auth.logout(request)
        messages.success(request, 'Logged out successfully')
        return redirect('index')
