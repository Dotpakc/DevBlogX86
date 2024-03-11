from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm



# Create your views here.
def login_view(request):
    form = AuthenticationForm()    
    return render(request, 'members/login.html', {'form': form})