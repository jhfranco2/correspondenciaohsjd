from django.shortcuts import render
from django.core.paginator import Paginator

from correspondencia.models import Libro,Ci,Zand,Gand

#Vista del inicio
def inicio(request):
    return render(request,'libros/inicio.html')

def libros(request, sigla=None):
    elementos_por_pagina =  7
    #preguntamos la sigla y mostramos el contenido 
    if sigla:
        libros = Libro.objects.filter(sigla=sigla)[::-1]
    else:
        libros = Libro.objects.all()[::-1]

    paginator = Paginator(libros, elementos_por_pagina)
    pagina = request.GET.get('pagina')
    libros_paginados = paginator.get_page(pagina)

    return render(request, 'libros/correspondencia.html', {
        "libros": libros_paginados
    })