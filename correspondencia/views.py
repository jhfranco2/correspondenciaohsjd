from django.shortcuts import render

#Vista del inicio
def inicio(request):
    return render(request,'libros/inicio.html')
