from django.shortcuts import redirect, render
from .models import BackFile, FrontFiles
from .forms import DeckForm
from django.conf import settings
from . import cards_placer
from os.path import join
import os
from django.views.static import serve
from django.http import HttpRequest
import shutil


def file_loader(request: HttpRequest):
    message_up = 'Upload your playing card decks, each front file of the deck should be inside a folder.\nYou should then select a back file and a name for the deck (group of cards) to identify it!'
    message_down = 'Select export parameters and download the files.'
    if request.session.session_key is None:
        request.session.save()
    session_key = request.session.session_key

    # Handle file upload
    if request.method == 'POST' and 'upload' in request.POST:
        form = DeckForm(request.POST, request.FILES)
        if form.is_valid():
            group_name = request.POST['name']
            if 'back' in request.FILES and 'fronts' in request.FILES:
                newdoc = BackFile(back=request.FILES['back'], group_name=group_name, session_id=session_key, short_name=f'{group_name}/back')
                newdoc.save()

                for front in request.FILES.getlist('fronts'):
                    newdoc = FrontFiles(front=front, group_name=group_name, session_id=session_key, short_name=f'{group_name}/front')
                    newdoc.save()


            # Redirect to the document list after POST
            return redirect('file_loader')
        else:
            message_up = 'The form is not valid. Fix the following error:'

    elif request.method == 'POST' and 'Delete' in request.POST.values():
        group_to_delete = ''
        for k in request.POST.keys():
            if request.POST[k] == 'Delete':
                group_to_delete = k
        print(group_to_delete)
        message_up += f' {group_to_delete} has been deleted!'
        BackFile.objects.filter(group_name=group_to_delete).delete()
        FrontFiles.objects.filter(group_name=group_to_delete).delete()
        session_dir = join(settings.MEDIA_ROOT, 'documents', session_key)

        shutil.rmtree(join(session_dir, 'backs', group_to_delete))
        shutil.rmtree(join(session_dir, 'fronts', group_to_delete))

        form = DeckForm()


    elif request.method == 'GET' and 'confirm&download' in request.GET:
        # plotter_format = request.GET.get('plotter_formats', None)
        plotter_height = int('0' + request.GET.get('plotter_height'))
        # if plotter_format is not None:
        if plotter_height is not None:
            plotter_width = int('0' + request.GET.get('plotter_width'))
            
            # cf = cards_formats.get_h_w_mm_from_format(request.GET.get('cards_formats', None))
            cards_height = int('0' + request.GET.get('cards_height'))
            cards_width = int('0' + request.GET.get('cards_width'))

            pad = int('0' + request.GET.get('padding', 0))
            um = request.GET.get('unit_of_measurement', None)
            cut_lines = request.GET.get('cut_lines', False)
            frame_lines = request.GET.get('frame_lines', False)

            session_dir = join(settings.MEDIA_ROOT, 'documents', session_key)

            print([plotter_height, plotter_width, cards_height, cards_width, pad, frame_lines, um])

            if os.path.exists(session_dir):
                filepath = cards_placer.get_output_file(session_dir, plotter_height, plotter_width, cards_height, cards_width, pad, frame_lines, um)
                # filepath = cards_placer.get_output_file(session_dir, plotter_format, cf[0], cf[1], pad, frame_lines, um)
                return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
            else:
                message_down += 'You need to upload some decks first!!!'


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
    context = {'backs_fronts': zip(backs, filtered_fronts), 'form': form, 'message_up': message_up, 'message_down': message_down}
    return render(request, 'main_page.html', context)

