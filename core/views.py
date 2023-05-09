from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect,render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView  #uses model forms
from django.urls import reverse_lazy
from .models import Task
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin #to restrict anyone going to other pages without logging in
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

class Login(LoginView):
    template_name = 'core/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    def get_success_url(self):
        return reverse_lazy('home')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            login(request,user)
            messages.success(request, "User Registered Succesfully")
            return redirect('/')
    else:
        form =UserCreationForm()

    context = {'form': form}
    return render(request, 'core/register.html', context)



class ListTask(LoginRequiredMixin, ListView):
    model=Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        return context

    def get_queryset(self):
        query = self.request.GET.get('search_item')
        if query:
            object_list = self.model.objects.filter(title__icontains=query)
            if object_list:
                return object_list
            else:
                messages.info(self.request, "No search results")
        else:
            object_list = self.model.objects.all()
        return object_list



class DetailTask(LoginRequiredMixin, DetailView):
    model=Task
    template_name = 'core/detail.html'
    context_object_name = 'tasks'

class CreateTask(LoginRequiredMixin, CreateView):  #creates modelform to create new item
    model=Task
    fields = ['title','desc','date']
    success_url = reverse_lazy('home') # name in view

    def form_valid(self, form):
        form.instance.user=self.request.user
        form.instance.status='pending'
        return super(CreateTask,self).form_valid(form)


class UpdateTask(LoginRequiredMixin,UpdateView):  #creates modelform to create new item
    model=Task
    fields = ['title','desc','date','status']
    success_url = reverse_lazy('home') # name in view

class DeleteTask(LoginRequiredMixin, DeleteView):
    model=Task
    template_name = 'core/delete.html'
    context_object_name = 'tasks'
    success_url = reverse_lazy('home')

