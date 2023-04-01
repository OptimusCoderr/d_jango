from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from .models import Room, Topic,Message
from .forms import RoomForm,UserForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
"""""
rooms=[
    {'id':1, 'name':"Let's learn python"},
    {'id':2, 'name':"Design with me"},
    {'id':3, 'name':"Frontend developers"},
]
"""""
def LoginPage(request): 
    page= 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method=='POST': # THIS MEANS THE USER LOGIN THEIR INFORMATION
        username=request.POST.get('username').lower()
        password=request.POST.get('password')

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,'User NOT Found.')

        user= authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Username or Password does not exist.')

    context={'page':page}
    return render(request, 'myass/login_register.html',context)

def LogoutUser(request):
    logout(request)
    return redirect('home')

def RegisterPage(request):
    #page='register'
    form= UserCreationForm()
    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user= form.save(commit=False)# commis=FALSE is to get the user object
            user.username=user.username.lower()# changing  the username to lower case
            user.save()
            login (request, user)
            return redirect('home')
        else:
            messages.error(request,'An error occurred during registration')

    return render(request,'myass/login_register.html',{'form':form})

def home(request):
    q= request.GET.get('q') if request.GET.get('q') !=None else ''
    rooms= Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)) #this code is for searching
    #rooms= Room.objects.all() # gives all the rooms in the datatbase 
    
    room_count= rooms.count()
    topics=Topic.objects.all()[0:5]
    room_messages=Message.objects.filter(Q(room__topic__name__icontains=q))


    context={'rooms':rooms,'topics':topics, 'room_count':room_count, 'room_messages':room_messages}
    return render(request, 'myass/home.html',context)

def room(request,pk):

    """""
    room= Nones
    for i in rooms:
        if i['id']==int(pk):
            room=i
     """""
    room=Room.objects.get(id=pk)# specify a unique value
    room_messages=room.message_set.all()#.order_by('-created')
    participants= room.participants.all()

    if request.method=="POST":
        message=Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body'),
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    

    context={'room':room, 'room_messages':room_messages,'participants':participants}
    return render(request, 'myass/room.html',context)

def userProfile(request,pk):
    user=User.objects.get(id=pk)
    rooms= user.room_set.all()
    room_messages=user.message_set.all()
    topics=Topic.objects.all()
    context={'user':user, 'rooms':rooms, 'room_messages': room_messages,'topics':topics}
    return render(request, 'myass/profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    form= RoomForm()
    topics=Topic.objects.all()
    if request.method=='POST':
        topic_name=request.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        
        )
        """""
        form=RoomForm(request.POST)
        if form.is_valid():
            room=form.save(commit=False)
            room.host=request.user
            room.save()
        """""
        return redirect('home')

    context={'form':form, 'topics':topics}
    return render(request,'myass/room_form.html',context)


@login_required(login_url='login')

def UpdateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    topics=Topic.objects.all()


    if request.method=='POST':
        topic_name=request.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)
        room.name= request.POST.get('name')
        room.topic= topic
        room.description= request.POST.get('description')
        room.save()
        """""
        form= RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            
        """""
        return redirect('home')
    
    context={'form':form,'topics':topics, 'room':room}
    return render(request,'myass/room_form.html', context)


@login_required(login_url='login')
def DeleteRoom(request,pk):
    room= Room.objects.get(id=pk)

    if request.user!= room.host :
        return HttpResponse('You are not allowed here!!')

    if request.method =="POST":
        room.delete()
        return redirect('home')
    return render(request,'myass/delete.html',{'obj':room})


#DELETE MESSAGE
@login_required(login_url='login')

def deleteMessage(request,pk):
    message= Message.objects.get(id=pk)

    if request.user!= message.user :
        return HttpResponse('You are not allowed here!!')

    if request.method =="POST":
        message.delete()
        return redirect('home')
    return render(request,'myass/delete.html',{'obj':message})


@login_required(login_url='login')
def updateUser(request):
    user=request.user
    form=UserForm(instance=user)

    if request.method=="POST":
        form=UserForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('userProfile',pk=user.id)

    context={'form':form}
    return render(request, 'myass/update_user.html',context)

def topicPage(request):
    q= request.GET.get('q') if request.GET.get('q') !=None else ''
    topics=Topic.objects.filter(name__icontains=q)

    context={"topics":topics}
    return render(request,'myass/topics.html',context)

def activityPage(request):
    room_messages=Message.objects.all()
    context={'room_messages':room_messages}
    return render(request,"myass/activity.html",context)

