from django.urls import path
from . import views

urlpatterns = [
   path('',views.inicio, name='inicio'),
   path('libros/',views.libros,name='correspondencia'),
   path('libros/<str:sigla>/',views.libros,name='correspondencia_por_sigla'),
   path('crear',views.crear,name='crear'),
   path('editar/<int:id>/', views.editar, name='editar'),
   path('eliminar/<int:id>/', views.eliminar, name='eliminar'),
]
