from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from chat.models import Room, Message

from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import *
from .forms import CreateUserForm, PostForm

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic import DetailView



def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')

        context = {'form': form}
        return render(request, 'chat/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'chat/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    return render(request, 'chat/dashboard.html')



def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'chat/room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })



def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/' + room + '/?username=' + username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/' + room + '/?username=' + username)


def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')


def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages": list(messages.values())})



class PostImage(TemplateView):

    form = PostForm
    template_name = 'chat/posts.html'

    def post(self, request, *args, **kwargs):

        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            obj = form.save()
            return HttpResponseRedirect(reverse_lazy('post_image_display', kwargs={'pk': obj.id}))

        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class PostImageDisplay(DetailView):
    model = Post
    template_name = 'chat/post_image_display.html'
    context_object_name = 'post'

"""def PostImage(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = PostForm()
    return render(request, 'chat/posts.html', {'form': form})

def success(request):
    return HttpResponse('successfully uploaded')
"""

"""def PostImageDisplay(request):
    if request.method == 'GET':
        # getting all the objects of hotel.
        Posts = Post.objects.all()

        return render(request, 'chat/post_image_display.html', {'Posts': Posts})

"""




