from django.urls import path
from . import views

urlpatterns = [
   path('',views.inicio, name='inicio'),
   path('libros/',views.libros,name='correspondencia'),
   path('libros/<str:sigla>/',views.libros,name='correspondencia_por_sigla'),
]
