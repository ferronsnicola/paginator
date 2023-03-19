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
    message_up = 'Upload your playing card decks, each front file of the deck should be inside a folder.\nYou should then select a back file and a name for the deck (groupd of cards) to identify it!'
    message_down = 'Select export parameters and download the files'
    if request.session.session_key is None:
        request.session.save()
    session_key = request.session.session_key

    # Handle file upload
    if request.method == 'POST' and 'upload' in request.POST:
        form = DeckForm(request.POST, request.FILES)
        if form.is_valid():
            group_name = request.POST['name']
            newdoc = BackFile(back=request.FILES['back'], group_name=group_name, session_id=session_key, short_name=f'{group_name}/back')
            newdoc.save()

            for front in request.FILES.getlist('fronts'):
                newdoc = FrontFiles(front=front, group_name=group_name, session_id=session_key, short_name=f'{group_name}/front')
                newdoc.save()


            # Redirect to the document list after POST
            return redirect('file_loader')
        else:
            message_up = 'The form is not valid. Fix the following error:'
    elif request.method == 'GET' and 'confirm&download' in request.GET:
        plotter_format = request.GET.get('plotter_formats', None)
        if plotter_format is not None:

            cf = cards_formats.get_h_w_mm_from_format(request.GET.get('cards_formats', None))

            pad = int(request.GET.get('padding', 0))
            um = request.GET.get('unit_of_measurement', None)
            cut_lines = request.GET.get('cut_lines', False)
            frame_lines = request.GET.get('frame_lines', False)

            filepath = cards_placer.get_output_file(join(settings.MEDIA_ROOT, 'documents', session_key), plotter_format, cf[0], cf[1], pad, frame_lines, um)
            return serve(request, os.path.basename(filepath), os.path.dirname(filepath))


        form = DeckForm()
    else:
        form = DeckForm()  # An empty, unbound form

    # Load documents for the list page
    backs = BackFile.objects.filter(session_id=session_key)
    fronts = FrontFiles.objects.filter(session_id=session_key)

    already_checked = set()
    filtered_fronts = []
    for front in fronts:
        if front.short_name not in already_checked:
            filtered_fronts.append(front)
            already_checked.add(front.short_name)



    # Render list page with the documents and the form
    context = {'backs': backs, 'fronts': filtered_fronts, 'form': form, 'message_up': message_up, 'message_down': message_down}
    return render(request, 'main_page.html', context)

