from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .forms import DocumentForm
from .models import Document, DocType, Origin
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator
import os
from django.http import HttpResponse
import mimetypes

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': AuthenticationForm, })

    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password']
        )

        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrecto'})
        else:
            login(request, user)
            return redirect('home')


def signup(request):
    # if request.method == 'GET':
    #     return render(request, 'signup.html', {'form': UserCreationForm})
    # else:
    #     if request.POST['password1'] == request.POST['password2']:
    #         try:
    #             user = User.objects.create_user(
    #                 username=request.POST['username'], password=request.POST['password1'])
    #             user.save()
    #             login(request, user) 
    #             return redirect('home')
    #         except IntegrityError:
    #             return render(request, 'signup.html', {
    #                 'form': UserCreationForm,
    #                 'error': 'Usuario ya existe'})

    #     return render(request, 'signup.html', {
    #         'form': UserCreationForm,
    #         'error': 'Las contraseñas no coinciden'})

    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm()})
    else:
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        # Verifica si los campos obligatorios están vacíos
        if not (username and password1 and password2):
            return render(request, 'signup.html', {
                'form': UserCreationForm(),
                'error': 'Por favor, completa todos los campos'})
        
        if password1 == password2:
            try:
                user = User.objects.create_user(username=username, password=password1)
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm(),
                    'error': f'El usuario {username} ya existe',
                    })
        else:
            return render(request, 'signup.html', {
                'form': UserCreationForm(),
                'error': 'Las contraseñas no coinciden'})


def home(request):
    return render(request, 'index.html')


@login_required
def signout(request):
    logout(request)
    return redirect('home')


@login_required
def registerdoc(request):
    if request.method == 'GET':
        form = DocumentForm()  
        return render(request, 'registerdoc.html', {'form': form})
    else:
        form = DocumentForm(request.POST, request.FILES) 
        if form.is_valid():  
            form.instance.user = request.user  
            form.save() 
            return redirect(reverse('registerdoc') + '?ok')
        else:
            return render(request, 'registerdoc.html', {'form': form})

@login_required
def searchdoc(request):
    doctypes = DocType.objects.all()
    origins = Origin.objects.all()

    dateregister = request.GET.get('date_search', '')
    doctype = request.GET.get('doctype_search', '')
    origin = request.GET.get('origin_search', '')
    description = request.GET.get('name_search', '')

    if any([dateregister, doctype, origin, description]):
        search_filters = {
            'dateregister': dateregister,
            'doctype': doctype,
            'origin': origin,
            'description': description,
        }
        request.session['search_filters'] = search_filters
    else:
        request.session.pop('search_filters', None)

    search_filters = request.session.get('search_filters', {})

    if search_filters:
        list_docs = Document.objects.order_by('dateregister').filter(description__icontains=description,
                                            doctype__id__icontains=doctype,
                                            dateregister__icontains=dateregister,
                                            origin__id__icontains=origin,
                                            user=request.user
                                            )
    else:
        list_docs = Document.objects.filter(user=request.user)

    paginator = Paginator(list_docs, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'paginator': paginator,
        'doctypes': doctypes,
        'origins': origins,
    }

    return render(request, 'searchdoc.html', context)


@login_required
def updatedoc(request, doc_id):
    document = get_object_or_404(Document, pk=doc_id, user=request.user)

    if request.method == 'GET':
        formatted_dateregister = document.dateregister.strftime('%Y-%m-%d')
        
        form = DocumentForm(instance=document, initial={'dateregister': formatted_dateregister})
        return render(request, 'updatedoc.html', {'document': document, 'form': form})
    
    else:
        try:
            document = get_object_or_404(
                Document, pk=doc_id, user=request.user)

            if len(request.FILES) != 0:
                if len(document.fileupload) > 0:
                    os.remove(document.fileupload.path)
                document.fileupload = request.FILES['fileupload']

            document.dateregister = request.POST["dateregister"]
            document.doctype= DocType.objects.get(pk=request.POST["doctype"])
            document.description = request.POST["description"]
            document.folios = request.POST["folios"]
            document.origin = Origin.objects.get(pk=request.POST["origin"])
            document.save()

            request.session['search_filters'] = request.GET.dict()

            messages.success(request, 'Documento actualizado con éxito')
            return redirect('searchdoc')

        except ValueError:
            return render(request, 'updatedoc.html', {
                'document': document,
                'form': form,
                'error': 'Error actualizado documento'})


@login_required
def deletedoc(request, doc_id):
    document = get_object_or_404(
        Document, pk=doc_id, user=request.user)

    if len(document.fileupload) > 0:
        os.remove(document.fileupload.path)

    document.delete()
    messages.success(request, 'Documento eliminado con éxito')
    return redirect('searchdoc')


@login_required
def previewdoc(request, doc_id):

    document = get_object_or_404(Document, pk=doc_id, user=request.user)
    pdf_path = document.fileupload.path
    with open(pdf_path, 'rb') as pdf_file:
        pdf_content = pdf_file.read()

    content_type, _ = mimetypes.guess_type(pdf_path)
    if not content_type:
        content_type = 'application/pdf'

    response = HttpResponse(pdf_content, content_type=content_type)
    response['Content-Disposition'] = 'inline; filename="{}"'.format(
        os.path.basename(pdf_path))
    return response

def error_404(request, exception):
    return render(request, '404.html', {})