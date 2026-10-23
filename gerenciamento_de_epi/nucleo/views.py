from django.shortcuts import render

# Create your views here.
def home(req):
    return render(req, 'base.html')

def emprestimos(req):
    return render(req, 'emprestimos.html')
    
def colaboradores(req):
    return render(req, 'colaboradores.html')