from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def loginForAdmin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        chek = authenticate(username=username, password=password)
        if chek is not None:
            login(request, chek)
            if chek.is_superuser == True:
                data = 'index_boss_url'
            else:
                data = 'index_url'
            return redirect(data)
        else:
            return redirect('login_url')
    else:
        return render(request, 'accaunts/login.html')

def  logoutForAdmin(request):
    logout(request)
    return redirect('kitchen_index_url')