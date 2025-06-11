from django.shortcuts import render

# Create your views here.
def alunos_view(request):
    return render(request, template_name='alunos.html', context={})
