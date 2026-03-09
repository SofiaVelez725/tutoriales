from django.shortcuts import render

def inicio(request):
	contexto = {
		'titulo': 'Tutorial Django - Vista Controlador',
		'mensaje': 'Proyecto creado paso a paso en la carpeta tutoriales.',
	}
	return render(request, 'core/inicio.html', contexto)
