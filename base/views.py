from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message, User, Poll, Option
from .forms import RoomForm, UserForm, MyUserCreationForm, PollForm, OptionForm
from datetime import datetime, timezone

# Create your views here.

# rooms = [
#     {'id': 1, 'name': 'Lets learn python!'},
#     {'id': 2, 'name': 'Design with me'},
#     {'id': 3, 'name': 'Frontend developers'},
# ]


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/login_register.html', {'form': form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q))[0:3]
    leaf_counts = sum([len(topic.room_set.all()) for topic in Topic.objects.all()])

    active_polls = Poll.objects.filter(completed=False).order_by('-time_end')
    active_polls_count = active_polls.count()
    active_polls = active_polls[0:3]
    print(active_polls)
    context = {'rooms': rooms, 'topics': topics,
               'room_count': room_count, 'room_messages': room_messages, 'active_polls': active_polls, 'leaf_counts': leaf_counts, 'active_polls_count': active_polls_count}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    print(room.has_poll)
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    return render(request, 'base/room.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms,
               'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form})


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    leaf_counts = sum([len(topic.room_set.all()) for topic in topics])

    return render(request, 'base/topics.html', {'topics': topics, 'leaf_counts':leaf_counts})


def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})

def allPolls(request):
    all_polls = Poll.objects.all()
    all_active_polls = Poll.objects.filter(completed=False).order_by('-time_end')
    return render(request, 'base/polls_all.html', {'all_polls': all_polls, 'all_active_polls': all_active_polls})


def poll(request, pk):
    
    room = Room.objects.get(id=pk)
    time_left = 0
    try:
        poll = Poll.objects.get(room=room)
        print(poll.question)
        options = poll.option_set.all()
        # [print(option.text)for option in  options]
        labels = [option.text for option in options]
        vote_counts = [option.user_selections.count() for option in options]
        print(labels)
        print(vote_counts)
        
        
        
        if poll.time_end <= datetime.now().replace(tzinfo=timezone.utc):
            if(poll.completed==False):
                poll.completed = True
                poll.save()
        else:
            time_left = poll.time_end - datetime.now().replace(tzinfo=timezone.utc)
    except:
        poll = {}
        options = {}
    return render(request, 'base/poll.html', {'poll':poll, 'labels':labels, 'vote_counts':vote_counts, 'time_left': time_left})

@login_required(login_url='login')
def createPoll(request, pk):
    form = PollForm()
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        Poll.objects.create(
            host=request.user,
            room=room,
            question=request.POST.get('question'),
            time_end=request.POST.get('time_end'),
        )
        room.has_poll = True
        room.save()
        return redirect('room', pk=room.id)

    context = {'form': form}
    return render(request, 'base/poll_form.html', context)

@login_required(login_url='login')
def createOption(request, pk):
    form = OptionForm()
    room = Room.objects.get(id=pk)
    poll = Poll.objects.get(room=room)
    if request.method == 'POST':
        Option.objects.create(
            question=poll,
            text=request.POST.get('text')
        )
        return redirect('poll', pk=room.id)

    context = {'form': form, 'poll': poll}
    return render(request, 'base/option_form.html', context)

@login_required(login_url='login')
def votePage(request, pk):
    room = Room.objects.get(id=pk)
    poll = Poll.objects.get(room=room)
    options = poll.option_set.all()
    if(request.user in poll.poll_takers.all()):
        request.session['voted'] = Option.objects.get(user_selections=request.user, question=poll).text
        return redirect('voted-already', pk=room.id)
    if request.method == 'POST':
        if(request.user not in poll.poll_takers.all()):
            poll.poll_takers.add(request.user)
            option = Option.objects.get(id=request.POST.get('option'))  
            option.user_selections.add(request.user)
        
            
        return redirect('poll', pk=room.id)

    context = {'poll': poll, 'options': options}
    return render(request, 'base/vote.html', context)

def votedAlready(request, pk):
    room = Room.objects.get(id=pk)
    poll = Poll.objects.get(room=room)
    context = {'poll': poll, 'room': room}
    return render(request, 'base/voted_already.html', context)