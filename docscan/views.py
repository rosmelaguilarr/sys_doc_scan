from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .forms import DocumentForm
from .models import Document
from django.urls import reverse
from django.contrib import messages
import os
import base64
from django.core.paginator import Paginator
from django.http import Http404


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
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)  # crear cookie
                return redirect('home')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Usuario ya existe'})

        return render(request, 'signup.html', {
            'form': UserCreationForm,
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
        return render(request, 'registerdoc.html', {
            'form': DocumentForm,
        })
    else:
        try:
            dateregister = request.POST["dateregister"]
            doctype = request.POST["doctype"]
            description = request.POST["description"]
            folios = request.POST["folios"]
            origin = request.POST["origin"]
            fileupload = request.FILES["fileupload"]

            new_document = Document(
                dateregister=dateregister, doctype=doctype, description=description, folios=folios,
                origin=origin, fileupload=fileupload, user=request.user)
            new_document.save()

            return redirect(reverse('registerdoc')+'?ok')

        except ValueError:
            return render(request, 'registerdoc.html', {
                'form': DocumentForm,
                'error': 'Por favor escribir información válida',
            })


@login_required
def searchdoc(request):

        dateregister = request.GET.get('date_search', '')
        doctype = request.GET.get('doctype_search', '')
        origin = request.GET.get('origin_search', '')
        description = request.GET.get('name_search', '')

        if not any([dateregister, doctype, origin, description]):
            return render(request, 'searchdoc.html')

        list_docs = Document.objects.filter(description__icontains=description,
                                            doctype__icontains=doctype,
                                            dateregister__icontains=dateregister,
                                            origin__icontains=origin,
                                            user=request.user
                                            )

        paginator = Paginator(list_docs, 2)  

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
            'paginator': paginator,
        }
        return render(request, 'searchdoc.html', context)


@login_required
def updatedoc(request, doc_id):
    if request.method == 'GET':
        document = get_object_or_404(Document, pk=doc_id, user=request.user)
        form = DocumentForm(instance=document)
        return render(request, 'updatedoc.html', {'document': document, 'form': form, })
    else:
        try:
            document = get_object_or_404(
                Document, pk=doc_id, user=request.user)

            if len(request.FILES) != 0:
                if len(document.fileupload) > 0:
                    os.remove(document.fileupload.path)
                document.fileupload = request.FILES['fileupload']

            document.dateregister = request.POST["dateregister"]
            document.doctype = request.POST["doctype"]
            document.description = request.POST["description"]
            document.folios = request.POST["folios"]
            document.origin = request.POST["origin"]
            document.save()

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

    # document = get_object_or_404(
    #     Document, pk=doc_id, user=request.user)

    # pdf_path = document.fileupload.path
    # with open(pdf_path, 'rb') as pdf_file:

    #     pdf_content = base64.b64encode(pdf_file.read()).decode()

    # context = {
    #     'pdf': pdf_content,
    # }

    # return render(request, "previewdoc.html", context)
    

    document = get_object_or_404(Document, pk=doc_id, user=request.user)
    pdf_path = document.fileupload.path

    # Crear una lista para almacenar los fragmentos codificados en base64
    pdf_content_chunks = []

    # Leer el archivo PDF en bloques y codificar cada bloque en base64
    with open(pdf_path, 'rb') as pdf_file:
        while True:
            # Leer un bloque de datos del archivo
            chunk = pdf_file.read(1024)  # Lee 1 KB a la vez

            # Si no hay más datos en el archivo, detener el bucle
            if not chunk:
                break

            # Codificar el bloque en base64 y agregarlo a la lista de fragmentos
            pdf_content_chunks.append(base64.b64encode(chunk).decode())

    # Concatenar los fragmentos codificados en base64 en una cadena
    pdf_content = ''.join(pdf_content_chunks)

    context = {
        'pdf': pdf_content,
    }

    return render(request, "previewdoc.html", context)