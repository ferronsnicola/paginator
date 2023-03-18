from django.shortcuts import redirect, render
from .models import BackFile, FrontFiles
from .forms import DeckForm
from django.conf import settings
from . import cards_placer
from . import cards_formats
from os.path import join
import os
from django.views.static import serve
from django.http import HttpRequest


def file_loader(request: HttpRequest):
    message = 'Upload as many files as you want!'
    if request.session.session_key is None:
        request.session.save()
    session_key = request.session.session_key

    # Handle file upload
    if request.method == 'POST' and 'upload' in request.POST:
        form = DeckForm(request.POST, request.FILES)
        if form.is_valid():
            group_name = request.POST['name']
            newdoc = BackFile(back=request.FILES['back'], group_name=group_name, session_id=session_key)
            newdoc.save()

            for front in request.FILES.getlist('fronts'):
                newdoc = FrontFiles(front=front, group_name=group_name, session_id=session_key)
                newdoc.save()


            # Redirect to the document list after POST
            return redirect('file_loader')
        else:
            message = 'The form is not valid. Fix the following error:'
    elif request.method == 'GET' and 'confirm&download' in request.GET:
        plotter_format = request.GET.get('plotter_formats', None)
        if plotter_format is not None:

            cf = cards_formats.get_h_w_mm_from_format(request.GET.get('cards_formats', 'AAA'))

            pad = int(request.GET.get('padding', 0))
            um = request.GET.get('unit_of_measurement', 'AAA')
            cut_lines = request.GET.get('cut_lines', False)
            frame_lines = request.GET.get('frame_lines', False)

            filepath = cards_placer.get_output_file(join(settings.MEDIA_ROOT, 'documents'), plotter_format, cf[0], cf[1], pad, frame_lines, um)
            return serve(request, os.path.basename(filepath), os.path.dirname(filepath))


        form = DeckForm()
    else:
        form = DeckForm()  # An empty, unbound form

    # Load documents for the list page
    documents = BackFile.objects.filter(session_id=session_key)

    # Render list page with the documents and the form
    context = {'documents': documents, 'form': form, 'message': message}
    return render(request, 'list.html', context)

