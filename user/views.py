from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages

#funções de views

def register(request):
    if request.method == 'POST':
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        
        if is_null(username):
            messages.error(request, 'Invalid username')
            return redirect('register')
        if is_null(password):
            message.error(request, 'Invalid password')
            return redirect('register')
        if password != confirmation:
            messages.error(request, 'As senhas precisam ser iguais iguais')
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Usuário já cadastrado')
            return redirect('register')
        
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        messages.success(request, "Cadastro realizado com sucesso!")

    return render(request, 'login.html')

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')

    if request.method == 'POST':
        email = request.POST['email']
        
        password = request.POST['password']
        
    if email == "" or password =="":
        messages.error(request, "Usuário ou senha inválidos!")
        return redirect('login')
    if User.objects.filter(email=email).exists():
        name = User.objects.filter(email=email).values_list('username', flat=True)
        user = auth.authenticate(request, username=name[0], password=password)
        
        if user is not None:
            auth.login(request, user)
            
        return redirect('index')
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    
    return redirect('index')



#Funções adicionais
def is_null(field):
    return not field.strip()