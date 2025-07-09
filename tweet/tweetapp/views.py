from django.shortcuts import render
from .models import tweet
from .forms import tweetForm,userRegistration
from django.shortcuts import get_object_or_404 ,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q

# Create your views here.
def index(request):
    return render(request, 'index.html')

def tweet_list(request):
    query = request.GET.get('q')
    tweets = tweet.objects.all().order_by('-created_at')
    if query:
        tweets = tweets.filter(
            Q(text__icontains=query) | Q(user__username__icontains=query)
        )
   

    return render(request, 'tweet_list.html', {
        'tweets': tweets,
        'query': query
    })

@login_required
def tweet_create(request):
    if request.method =='POST':
      form = tweetForm(request.POST,request.FILES)
      if form.is_valid():
          tweet1 = form.save(commit=False)
          tweet1.user = request.user
          tweet1.save()
          return redirect('tweet_list')
    else:
        form = tweetForm()
        return render(request, 'tweet_form.html',{'form':form})
    

@login_required
def tweet_edit(request,tweet_id):
    tweet1 = get_object_or_404(tweet,pk=tweet_id, user = request.user)
    if request.method =='POST':
      form = tweetForm(request.POST,request.FILES,instance=tweet1)
      if form.is_valid():
          tweet1 = form.save(commit=False)
          tweet1.user = request.user
          tweet1.save()
          return redirect('tweet_list')
    else:
        form = tweetForm(instance=tweet1)
        return render(request, 'tweet_form.html',{'form':form})

@login_required
def tweet_delete(request,tweet_id):
    tweet1 = get_object_or_404(tweet,pk=tweet_id,user = request.user)
    if request.method =='POST':
        tweet1.delete()
        return redirect('tweet_list')
    
    return render(request, 'tweet_delete_form.html',{'tweet':tweet1})

def register(request):
    if request.method == 'POST':
        form = userRegistration(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request , user)
            return redirect('tweet_list')
        
    else :
        form = userRegistration()

    return render(request, 'Registrations/register.html',{'form':form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next') or 'tweet_list'
            return redirect(next_url) 
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'Registrations/login.html')


def logout_view(request):
    logout(request)
    return render(request, 'Registrations/login.html')  
