from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from .forms import DocumentForm
from .models import Document, DocType, Direction
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator
import os
from django.http import HttpResponse, Http404
import mimetypes


def home(request):
    return render(request, 'index.html')


def signin(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Usuario o contraseña incorrecto')
    else:
        form = AuthenticationForm(
            initial={'username': request.POST.get('username', '')})

    return render(request, 'signin.html', {'form': form})


@login_required
def signout(request):
    logout(request)
    return redirect('home')


@login_required
@permission_required('docscan.add_document', raise_exception=True)
def registerdoc(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect(reverse('registerdoc') + '?ok')
    else:
        form = DocumentForm()

    return render(request, 'registerdoc.html', {
        'form': form,
    })


@login_required
def searchdoc(request):
    user_groups = request.user.groups.all()
    doctypes = DocType.objects.all()
    directions = Direction.objects.all()

    dateregister = request.GET.get('date_search', '')
    doctype = request.GET.get('doctype_search', '')
    id = request.GET.get('codigo_search', '')
    direction = request.GET.get('direction_search', '')
    description = request.GET.get('name_search', '')

    if any([dateregister, doctype, direction, id, description]):
        search_filters = {
            'dateregister': dateregister,
            'doctype': doctype,
            'direction': direction,
            'id': id,
            'description': description,
        }
        request.session['search_filters'] = search_filters
    else:
        request.session.pop('search_filters', None)

    search_filters = request.session.get('search_filters', {})

    if search_filters:
        list_docs = Document.objects.order_by('-id').filter(description__icontains=description,
                                                                 doctype__id__icontains=doctype,
                                                                 dateregister__icontains=dateregister,
                                                                 direction__id__icontains=direction,
                                                                 id__icontains=id,
                                                                 )
    else:
        list_docs = Document.objects.all().order_by('-id')

    documents = []
    for document in list_docs:
        document.file_exists = os.path.exists(document.fileupload.path)
        documents.append(document)
    
    paginator = Paginator(documents, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'paginator': paginator,
        'doctypes': doctypes,
        'directions': directions,
        'user_groups': user_groups,

    }

    return render(request, 'searchdoc.html', context)


@login_required
@permission_required('docscan.change_document', raise_exception=True)
def updatedoc(request, doc_id):
    document = get_object_or_404(Document, pk=doc_id)

    if request.method == 'GET':
        formatted_dateregister = document.dateregister.strftime('%Y-%m-%d')

        form = DocumentForm(instance=document, initial={
                            'dateregister': formatted_dateregister})

        return render(request, 'updatedoc.html',
                      {'document': document,
                       'form': form,

                       })

    else:
        try:
            document = get_object_or_404(
                Document, pk=doc_id)

            if len(request.FILES) != 0:
                if len(document.fileupload) > 0:
                    os.remove(document.fileupload.path)
                document.fileupload = request.FILES['fileupload']

            document.dateregister = request.POST["dateregister"]
            document.doctype = DocType.objects.get(pk=request.POST["doctype"])
            document.description = request.POST["description"]
            document.folios = request.POST["folios"]
            document.direction = Direction.objects.get(
                pk=request.POST["direction"])
            document.origin = request.POST["origin"]

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
@permission_required('docscan.delete_document', raise_exception=True)
def deletedoc(request, doc_id):
    document = get_object_or_404(Document, pk=doc_id)
    file_path = document.fileupload.path

    if not os.path.exists(file_path):
        raise Http404("El archivo no existe")

    if len(document.fileupload) > 0:
        os.remove(document.fileupload.path)

    document.delete()
    messages.success(request, 'Documento eliminado con éxito')
    return redirect('searchdoc')


@login_required
def previewdoc(request, doc_id):
    document = get_object_or_404(Document, pk=doc_id)
    pdf_path = document.fileupload.path

    if not os.path.exists(pdf_path):
        raise Http404("El archivo no existe")

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


def error_403(request, exception):
    return render(request, '403.html', status=403)
