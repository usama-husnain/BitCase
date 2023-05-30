from rest_framework.views import APIView
from rest_framework import generics
from django.views.generic import ListView,CreateView,DetailView,UpdateView,DeleteView
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import HttpResponse, render, redirect, get_list_or_404, get_object_or_404
from django.http import JsonResponse
from .models import Task, Post
from django.forms import ModelForm
from .serializers import TaskSerializer, PostSerializer
from django.urls import reverse_lazy
from rest_framework.authtoken.models import Token
from .validation import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

@login_required(login_url='/login')
def welcome(request):
    message = request.session['login']
    request.session['login'] = None
    return render(request, 'welcome.html',{'message':message})

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'desc', 'completed']

@login_required(login_url='/login')
def index(request):
    tasks = get_list_or_404(Task)
    return render(request, 'tasks/index.html', {'tasks':tasks})


def search(request):
    complete = int(request.POST.get('completed'))
    start_date = request.POST.get('start')
    end_date = request.POST.get('end')
    if(complete and start_date and end_date or complete==0 ):
        tasks = Task.objects.filter(created__date__range=(start_date, end_date), completed=complete)
        return render(request, 'tasks/index.html', {'tasks':tasks})
    else:
        messages.success(request, "Invalid search request! Please fill all fields.")
        return redirect('tasks')

def taskCompleted(request):
    id = request.POST.get('id')
    task = Task.objects.get(id=id)
    completed =int(request.POST.get('completed')) 
    task.completed=completed
    task.save()
    return JsonResponse({'success':1})


def view(request, id):
    task= get_object_or_404(Task, pk=id)  
    return render(request, 'tasks/view.html', {'task':task})


def create(request):
   return render(request, 'tasks/create.html')


def store(request):
#    return HttpResponse(request.POST)
   form = TaskForm(request.POST)
   if form.is_valid():
        form.save()
        return redirect('tasks')
   return render(request, 'tasks/create.html', {'form':form})


def update(request, id):
#    return HttpResponse("updated")
   task = Task.objects.get(id=id)
  
   if request.method == 'POST':
       form = TaskForm(request.POST, instance=task)
       if form.is_valid():
        form.save()
        return redirect('tasks')
   else:
       form = TaskForm(instance=task)

   return render(request, 'tasks/update.html', {'form':form, 'task': task})


def task_delete(request, id):
    task= get_object_or_404(Task, pk=id)  
    task.delete()
    return redirect('tasks')





class TaskAPIView(APIView):
    def get(self, request):
       tasks = Task.objects.all()
       serializer = TaskSerializer(tasks, many=True)
       return Response(serializer.data)
    
    def post(self, request):
       serializer = TaskSerializer(data=request.data)
       if serializer.is_valid():
           serializer.save()
           return Response(serializer.data, status=201)
       
       return Response(serializer.errors, status=400)
    
    def post(self, request):
       serializer = TaskSerializer(data=request.data)
       if serializer.is_valid():
           serializer.save()
           return Response(serializer.data, status=201)
       
       return Response(serializer.errors, status=400)
    
class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer



class PostListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    
    

class PostCreateView(CreateView):
   
    model = Post
    template_name = 'posts/post_create.html'
    form_class = PostFormValidation
    # fields = ['title', 'content']
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        return super().form_valid(form)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        # Set custom validation messages here
      
        # form.errors['title'] = form.error_class(['Title field is required!'])
        # form.add_error('content', 'Content field is required!')
        return response
    

class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

class PostUpdateView(UpdateView):
    model = Post
    template_name = 'posts/post_update.html'
    fields = ['title', 'content']
    context_object_name = 'post'

    def get_queryset(self):
        return super().get_queryset()

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'posts/post_delete.html'
    success_url = reverse_lazy('post_list')

    def get_queryset(self):
        return super().get_queryset()
    



class PostViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class  = PostSerializer