from django.shortcuts import render

# Create your views here.
def home(req):
    colaboradores = Colaboradores.objects.all()
    return render(req, 'home.html', {
        'colaboradores': colaboradores,
    })


def emprestimos(req):
    return render(req, 'emprestimos.html')
    
def colaboradores(req):
    return render(req, 'colaboradores.html')