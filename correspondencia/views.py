from io import BytesIO
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.contrib import messages
from correspondencia.forms import AuditoriaForm, LibroForm, MensajeriaForm
from correspondencia.models import Libro,Ci,Zand,Gand
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Paragraph
from reportlab.lib.pagesizes import letter,inch,landscape
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
from datetime import datetime


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


def reportes(request):
    return render(request,'libros/reportes.html')


def generar_reporte_mensajeria(request):
   # libros = Libro.objects.filter(fecha_entrada__range=['2023-04-05T00:00:00', '2023-04-05T13:00:00'],remitente_destinatario__istartswith= 'D')
    if request.method == 'POST':
        form = MensajeriaForm(request.POST)
        if form.is_valid():
            # procesar la fecha
            fecha_inicio = form.cleaned_data['fecha_inicio']
            fecha_fin = form.cleaned_data['fecha_fin']
            #buscar los libros
            libros_mensajeria =  Libro.objects.filter(
                fecha_entrada__range=[fecha_inicio,fecha_fin],
                remitente_destinatario__istartswith= 'D'
            )
            
            encabezado = [['id', 'sigla','fecha entrada','remitente destinatario','importancia','direccion','nombre destinatario remitente','asunto','salida','registro de entrega','observaciones']]
            data = []
            for libro in libros_mensajeria:
                if libro.sigla == 'Z':
                    id_relacionado = libro.zand.id
                elif libro.sigla == 'G':
                    id_relacionado = libro.gand.id
                elif libro.sigla == 'C':
                     id_relacionado = libro.ci.id
                else:
                    id_relacionado = 'ID desconocido'
                row = [
                    str(id_relacionado),
                    libro.sigla if libro.sigla is not None else '',
                    str(libro.fecha_entrada.strftime('%d/%m/%Y %H:%M')) if libro.fecha_entrada is not None else '',
                    libro.remitente_destinatario if libro.remitente_destinatario is not None else '',
                    libro.importancia if libro.importancia is not None else '',
                    libro.direccion if libro.direccion is not None else '',
                    libro.nombre_destinatario_remitente if libro.nombre_destinatario_remitente is not None else '',
                    libro.asunto if libro.asunto is not None else '',
                    str(libro.salida.strftime('%d/%m/%Y %H:%M')) if libro.salida is not None else '',
                    libro.registro_de_entrega if libro.registro_de_entrega is not None else '',
                    libro.observaciones if libro.observaciones is not None else '',
                     ]
                data.append(row)
            colWidths=[22,30,55,30,30,55,55,110,55,148.5,197]   
            return generar_pdf(encabezado + data,colWidths)           
    else:
        form = MensajeriaForm()
    return render(request,"reportes/mensajeria.html",{'form':form})

def generar_reporte_auditoria(request):
    if request.method == 'POST':
        form = AuditoriaForm(request.POST)
        if form.is_valid():
            # procesar la fecha
            fecha_inicio = form.cleaned_data['fecha_inicio']
            fecha_fin = form.cleaned_data['fecha_fin']
            #buscar los libros
            libros_mensajeria =  Libro.objects.filter(
                fecha_entrada__range=[fecha_inicio,fecha_fin],
                remitente_destinatario__istartswith= 'D'
            ).exclude(salida__isnull=True)           
            encabezado = [['id', 'sigla','fecha entrada','remitente destinatario','importancia','direccion','nombre destinatario remitente','asunto','salida','registro de entrega','observaciones','cumplio plazo']]
            data = []
            for libro in libros_mensajeria:
                if libro.sigla == 'Z':
                    id_relacionado = libro.zand.id
                elif libro.sigla == 'G':
                    id_relacionado = libro.gand.id
                elif libro.sigla == 'C':
                     id_relacionado = libro.ci.id
                else:
                    id_relacionado = 'ID desconocido'
                fecha_inicio_libro =  libro.fecha_entrada
                fecha_salida_libro = libro.salida 
                diferencia_horas = fecha_salida_libro - fecha_inicio_libro
                horas = diferencia_horas.total_seconds() // 3600              
                importancia =  libro.importancia
                if importancia == 'A':
                    plazo_horas = 4
                elif importancia == 'M':
                    plazo_horas == 24
                elif importancia == 'B':
                    plazo_horas = 72    
                else:
                    plazo_horas = 0
                # Verificar si se cumplió el plazo
                cumplio_plazo = 1 if horas <= plazo_horas else 0   
                row = [
                    str(id_relacionado),
                    libro.sigla if libro.sigla is not None else '',
                    str(libro.fecha_entrada.strftime('%d/%m/%Y %H:%M')) if libro.fecha_entrada is not None else '',
                    libro.remitente_destinatario if libro.remitente_destinatario is not None else '',
                    libro.importancia if libro.importancia is not None else '',
                    libro.direccion if libro.direccion is not None else '',
                    libro.nombre_destinatario_remitente if libro.nombre_destinatario_remitente is not None else '',
                    libro.asunto if libro.asunto is not None else '',
                    str(libro.salida.strftime('%d/%m/%Y %H:%M')) if libro.salida is not None else '',
                    libro.registro_de_entrega if libro.registro_de_entrega is not None else '',
                    libro.observaciones if libro.observaciones is not None else '',
                    str(cumplio_plazo)
                     ]
                data.append(row)
            colWidths=[22, 30, 55, 30, 30, 55, 55, 110, 55, 148.5, 160, 30]   
            return generar_pdf(encabezado+data,colWidths)           
    else:
        form = AuditoriaForm()
    return render(request,"reportes/auditoria.html",{'form':form})        

def generar_pdf(data,colWidths):
    # Crear un objeto de buffer de BytesIO
    buffer = BytesIO()
    
    #dimensiones de la pagina 
    page_size = landscape(letter)

    # Calcular la altura de cada fila para que haya un máximo de 7 filas por página
    max_rows_per_page = 8
    row_height = (page_size[1] - inch) / max_rows_per_page

    #estilos de los parrafos
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER, fontSize=8))

    #Crear una lista de objetos Paragraph para cada celda de la tabla
    data1_paragraphs = []

    #recorrer las filas y columnas para asignarles el estilo de párrafo
    for row in data:
        row_paragraphs = []
        for cell in row:
            row_paragraphs.append(Paragraph(cell, styles['Center']))
        data1_paragraphs.append(row_paragraphs) 
    # Crear la tabla
    tabla = Table(data1_paragraphs, colWidths, rowHeights=row_height)

    # Estilo de la tabla
    estilo_tabla = TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BOX', (0, 0), (-1, -1), 1, colors.black)
    ])
    
    # Modificar el estilo de la tabla basado en el valor de la última columna
    for i in range(1, len(data)):
        if data[i][-1] == '1':
         estilo_tabla.add('BACKGROUND', (-1, i), (-1, i), colors.green)
        elif data[i][-1] == '0':
         estilo_tabla.add('BACKGROUND', (-1, i), (-1, i), colors.red)
 
    
    # Aplicar el estilo a la tabla
    tabla.setStyle(estilo_tabla)

    # Generar el objeto canvas
    doc = SimpleDocTemplate(buffer, pagesize=page_size, topMargin=0)

    contenido = []
    contenido.append(tabla)
    doc.build(contenido)
    
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    return response        