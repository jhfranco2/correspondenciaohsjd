from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.contrib import messages
from correspondencia.forms import LibroForm
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

def crear(request):
    if request.method == 'POST':
        form = LibroForm(request.POST)
        if form.is_valid():
            libro = form.save(commit=False)
            sigla = form.cleaned_data['sigla']
            print(sigla)
            guardar_libro_y_dependencias(libro,sigla)
            return redirect('correspondencia')
    else:
        form = LibroForm()
    return render(request, 'libros/crear.html', {'forms': form})

def editar(request, id):
    libro = get_object_or_404(Libro, id=id)
    if request.method == 'POST':
        form = LibroForm(request.POST, instance=libro)
        if form.is_valid():
            libro = form.save(commit=False)
            sigla = form.cleaned_data['sigla']
            libro.save()
            if sigla != libro.sigla:
                # la sigla ha sido cambiada
                libro.dependencia.delete()
                guardar_libro_y_dependencias(libro, sigla)
            return redirect('correspondencia')
    else:
        form = LibroForm(instance=libro)
    return render(request, 'libros/editar.html', {'forms': form})

def eliminar(request, id):
    # Obtener el objeto que deseas eliminar
    libro = get_object_or_404(Libro, pk=id)
    

    if request.method == 'POST':
        # Verificar si se envió el parámetro "eliminar" en el cuerpo de la solicitud
        if request.POST.get('eliminar') == 'si':
            # Eliminar el objeto
            libro.delete()
            # Añadir mensaje de alerta
            messages.success(request, f'Se eliminó el objeto {id} correctamente.')
            # Redireccionar a una página de confirmación
            libros = Libro.objects.all()[::-1]
            return render(request,'libros/correspondencia.html',{"libros":libros})
        else:
            # Si el parámetro "eliminar" no está presente o es diferente a "si", retornar un error 400
            return HttpResponseBadRequest('La solicitud es inválida.')
    libros = Libro.objects.all()[::-1]
    # Si el método de la solicitud no es POST, mostrar la página de confirmación de eliminación
    return render(request,'libros/correspondencia.html',{"libros":libros})

def guardar_libro_y_dependencias(libro, sigla):
    # guardar el libro
    libro.save()

    # guardar la dependencia correspondiente según el tipo de documento
    if  sigla == 'C':
        ci = Ci(libro=libro)
        ci.save()
    elif sigla == 'Z':
        zand = Zand(libro=libro)
        zand.save()
    elif sigla == 'G':
        yand = Gand(libro=libro)
        yand.save()