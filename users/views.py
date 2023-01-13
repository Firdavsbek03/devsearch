from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .models import Profile, Message
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm, SkillForm,MessageForm
from django.contrib.auth.decorators import login_required
from .utils import search_profiles, paginate_profiles


def logout_user(request):
    messages.info(request, "User logged out successfully.")
    logout(request)
    return redirect('login')


def register_user(request):
    page = 'register'
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "User account has been created successfully!")
            login(request, user)
            return redirect('edit-account')
        else:
            messages.error(request, "An error has occurred during registration!")
    context = {'page': page, 'form': form, }
    return render(request, 'users/login_register.html', context=context)


def login_user(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('profiles')
    else:
        if request.method == "POST":
            username = request.POST['username'].lower()
            try:
                password = request.POST['password']
            except:
                password = request.POST['password1']
            try:
                user = User.objects.get(username=username)
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, "Logged in successfully!")
                    return redirect(request.GET['next'] if 'next' in request.GET else 'account')
                else:
                    messages.error(request, "Username and Password doesn't match.")
            except User.DoesNotExist:
                messages.warning(request, 'User doesn\'t exist in the database')
        return render(request, 'users/login_register.html', context={"page": page})


def get_profiles(request):
    search_query, profiles = search_profiles(request)
    profiles, custom_range = paginate_profiles(request, profiles, 3)
    context = {
        "profiles": profiles,
        "search_query": search_query,
        "custom_range": custom_range,
    }
    return render(request, 'users/profiles.html', context=context)


def get_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    top_skills = profile.skill_set.exclude(description__exact="")
    other_skills = profile.skill_set.filter(description='')
    return render(
        request,
        'users/user-profile.html',
        {
            "profile": profile,
            "top_skills": top_skills,
            'other_skills': other_skills,
        })


@login_required(login_url='login')
def user_account(request):
    profile = request.user.profile
    projects = profile.project_set.all()
    skills = profile.skill_set.all()
    context = {
        "profile": profile,
        "skills": skills,
        "projects": projects,
    }
    return render(request, 'users/account.html', context=context)


@login_required(login_url='login')
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
        return redirect('account')
    context = {"form": form}
    return render(request, 'users/profile_form.html', context=context)


@login_required(login_url='login')
def create_skill(request):
    profile = request.user.profile
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            return redirect('account')
    return render(request, 'users/skill_form.html', context={'form': form})


@login_required(login_url='login')
def update_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('account')
    return render(request, 'users/skill_form.html', {"form": form})


@login_required(login_url='login')
def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == "POST":
        skill.delete()
        return redirect('account')
    return render(request, 'delete_template.html', {"object": skill})


@login_required(login_url='login')
def inbox(request):
    profile=request.user.profile
    message_set = profile.messages.all()
    unread_messages=message_set.filter(is_read=False).count()
    context = {
        'messages': message_set,
        'unread_messages':unread_messages,
    }
    return render(request, 'users/inbox.html', context=context)


@login_required(login_url='login')
def view_message(request, pk):
    profile=request.user.profile
    message = profile.messages.get(id=pk)
    if not message.is_read:
        message.is_read=True
        message.save()
    context = {
        "message": message,
    }
    return render(request, 'users/message.html', context=context)


def create_message(request,pk):
    recipient=Profile.objects.get(id=pk)
    form = MessageForm()
    try:
        sender=request.user.profile
    except:
        sender=None

    if request.method=="POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            new_message=form.save(commit=False)
            new_message.sender=sender
            new_message.recipient=recipient

            if sender:
                new_message.name=sender.name
                new_message.email=sender.email

            new_message.save()
            return redirect('user_profile',pk=recipient.id)
    context={
        'form':form,
        'recipient':recipient,
    }
    return render(request,'users/message_form.html',context=context)
