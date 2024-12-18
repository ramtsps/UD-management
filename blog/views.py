from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
# Create your views here.
# def index(request):
#     return HttpResponse("Hello, world!")

# def data1(request,post_id):
#     return render(request,'index.html',{ 'post_id':post_id})
# def details(request,):
#     return render(request,'detail.html')



# def contact(request):
#     if request.method == 'POST':
#         # Retrieve form data
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         message = request.POST.get('message')

#         # Render the template with the provided data
#         return render(request, 'contact.html', {'name': name, 'email': email, 'message': message})

#     # Render the template for GET requests or others
#     return render(request, 'contact.html')




def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')  # Do not hash the password here
        try:
            # Safely query the database
            user = UserData.objects.get(username=username)

            # Check if the plain-text password matches the hashed password
            if check_password(password, user.password):
                # Save user info in session
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                request.session['profile_picture']=user.profile_picture.url
                messages.success(request, f"Welcome, {user.username}!")
                # login(request, user)
                return redirect('blog:index')  # Redirect to home or dashboard
            else:
                # Password mismatch
                messages.error(request, "Invalid password. Please try again.")
        except UserData.DoesNotExist:
            # User not found
            messages.error(request, "Username does not exist. Register or Please try again.")

    # Render the login form
    return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)  # Handle file uploads

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            email = form.cleaned_data['email']
            profile_picture = form.cleaned_data['profile_picture']  # Get the profile picture

            # Check if email already exists
            if UserData.objects.filter(email=email).exists():
                form.add_error('email', 'This email address is already taken.')
                return render(request, 'register.html', {'form': form})

            # Check if username is already taken
            if UserData.objects.filter(username=username).exists():
                form.add_error('username', 'This username is already taken.')
                return render(request, 'register.html', {'form': form})

            # Ensure passwords match
            if password == confirm_password:
                hashed_password = make_password(password)  # Hash password before saving
                # Create the user
                user = UserData.objects.create(
                    username=username,
                    password=hashed_password,
                    email=email,
                    profile_picture=profile_picture  # Save the profile picture if uploaded
                )
                messages.success(request, "Registration successful. You can now log in.")
                return redirect('blog:login')
            else:
                form.add_error('password', 'The passwords do not match.')
                messages.error(request, "The passwords do not match.")
                return render(request, 'register.html', {'form': form})
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form = RegisterForm()  # Display empty form for GET request
    return render(request, 'register.html', {'form': form})
def logout_view(request):
    if 'user_id' in request.session:
        del request.session['user_id']
        del request.session['username']
        del request.session['profile_picture']
        messages.success(request, "You have been logged out.")
    return redirect('blog:login')



def profile(request):
    if request.session.get('user_id') is None:
        return redirect('blog:login')
    user_id = request.session.get('user_id')
    user_profile = UserData.objects.get(id=user_id)

    print("image",user_profile.profile_picture)
    return render(request, 'profile.html', {'user': user_profile})

def edit_profile(request):
    # Get the user ID from the session and retrieve the user instance from the database
    user_id = request.session.get('user_id')
    if user_id is None:
        return redirect('blog:login')  # Redirect to login if no session found

    try:
        user = UserData.objects.get(id=user_id)  # Get the UserData instance
    except UserData.DoesNotExist:
        return redirect('blog:login')  # Redirect if user is not found

    # If the form is submitted
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        print("Form data:", request.POST)
        if form.is_valid():
            user = form.save()  # Save the updated user information

            # Update session with the new username and profile picture URL
            request.session['username'] = form.cleaned_data['username']
            if user.profile_picture:
                request.session['profile_picture'] = user.profile_picture.url
            else:
                request.session['profile_picture'] = None  # Or use a default image URL

            print("Form is valid")
            return redirect('blog:profile')  # Redirect to the profile page after successful update
        else:
            print("Form errors:", form.errors)  # Print form validation errors
    else:
        # Display the current user's information in the form
        form = UserProfileForm(instance=user)

    return render(request, 'edit_profile.html', {'form': form})


def index(request):
    data = Contact.objects.all()
    
    # Check if the 'user_id' is set in the session
    if request.session.get('user_id') is None:
        return redirect('blog:login')  # Redirect to the login page if no user is logged in
    
    # Proceed with rendering the page if the user is logged in
    return render(request, 'index.html', {"data": data})
  

    


def contact_view(request):
    if request.session.get('user_id') is None:
        return redirect('blog:login')  # Redirect to login if not logged in

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():  # Validate the form
            form.save()  # Save form data to the database
            messages.success(request, "Your message has been successfully submitted!")
            return redirect('blog:index')  # Redirect to index page on success
        else:
            messages.error(request, "There was an error with your submission. Please fix the errors below.")
    else:
        form = ContactForm()

    return render(request, 'contact_form.html', {'form': form})

def ListOut(request):
    if request.session.get('user_id') is None:
        return redirect('blog:login')  # Redirect to login if not logged in
    List = UserData.objects.all()
    return render(request, 'list_out.html', {"List": List})



def success_view(request ):
    return render(request, 'success.html', {'message': 'Form submitted successfully!'})



def update_view(request, id):
    if request.session.get('user_id') is None:
        return redirect('blog:login')
    # Get the contact object or return a 404 if not found
    data = get_object_or_404(Contact, id=id)
    
    if request.method == 'POST':
        # Handle form submission to update the record
        form = ContactForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            # Redirect to success page after saving
            messages.success(request, "Your data has been successfully updated.")
            return redirect('blog:index')  # Redirect to success page
    
    else:
        form = ContactForm(instance=data)  # Initialize the form with existing data
    
    return render(request, 'update_form.html', {'form': form, 'data': data})


def delete_view(request, id):
    # Get the contact object or return a 404 if not found
    data = get_object_or_404(Contact, id=id)
    data.delete()  # Delete the record
    return redirect('blog:index')  # Redirect to success page after deletion



 # Assuming the form is named this

def update_user_data(request, id):
    if request.session.get('user_id') is None:
        return redirect('blog:login')
    # Get the user object or return a 404 if not found
    data = get_object_or_404(UserData, id=id)
    
    if request.method == 'POST':
        form = RegisterForm_changes(request.POST, instance=data)

        # Handle password confirmation logic before saving
        if form.is_valid():
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            
            if password != confirm_password:
                form.add_error('password', 'The passwords do not match.')
                messages.error(request, "The passwords do not match.")
                return render(request, 'update_form.html', {'form': form, 'data': data})

            # If passwords match, hash the password and save the form
            data.password = make_password(password)
            form.save()
            messages.success(request, "Your data has been successfully updated.")
            return redirect('blog:ListOut')
        
    else:
        form = RegisterForm_changes(instance=data)  # Initialize the form with existing data
    
    return render(request, 'update_form_list.html', {'form': form, 'data': data})



def delet_user_data(request, id):
    # Get the contact object or return a 404 if not found
    data = get_object_or_404(UserData, id=id)
    data.delete()  # Delete the record
    return redirect('blog:ListOut')  # Redirect to success page after deletion


def custom_404(request,exception ):
    return render(request, '404.html', status=404)
def custom(request, ):
    return render(request, '404.html', status=404)