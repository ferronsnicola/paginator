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
from django.contrib import messages


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
        plotter_format = request.GET.get('plotter_formats', None)
        if plotter_format == 'manual':
            plotter_height = int('0' + request.GET.get('plotter_height'))
            plotter_width = int('0' + request.GET.get('plotter_width'))
        else:
            plotter_height, plotter_width = cards_placer.plotter_formats[plotter_format]
        
        cards_format = request.GET.get('cards_formats', None)
        if cards_format == 'manual':
            cards_height = int('0' + request.GET.get('cards_height'))
            cards_width = int('0' + request.GET.get('cards_width'))
        else:
            cards_height, cards_width = cards_placer.cards_formats[cards_format]

        pad = int('0' + request.GET.get('padding', 0))
        um = request.GET.get('unit_of_measurement', None)
        cut_lines = request.GET.get('cut_lines', False)
        frame_lines = request.GET.get('frame_lines', False)

        session_dir = join(settings.MEDIA_ROOT, 'documents', session_key)

        print([plotter_height, plotter_width, cards_height, cards_width, pad, frame_lines, um])

        logic_error = False
        error_message = ''

        if not cards_placer.check_consistency(cards_size=cards_height, pad=pad, bg_size=plotter_height):
            error_message += 'Plotter Height must be greater than Cards Height + 2 * Padding. '
            logic_error = True
        if not cards_placer.check_consistency(cards_size=cards_width, pad=pad, bg_size=plotter_width):
            error_message += 'Plotter Width must be greater than Cards Width + 2 * Padding. '
            logic_error = True
        # if get_spacing(plotter_height, cards_height)
        

        if not logic_error:
            if os.path.exists(session_dir):
                filepath = cards_placer.get_output_file(session_dir, plotter_height, plotter_width, cards_height, cards_width, pad, cut_lines, frame_lines, um)
                return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
            else:
                error_message += 'You need to upload some decks first!!!'
                logic_error = True
        
        if logic_error:
            messages.error(request=request, message=error_message)


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

    backs_fronts = None
    if len(backs) > 0:
        backs_fronts = zip(backs, filtered_fronts)

    # Render list page with the documents and the form
    context = {'backs_fronts': backs_fronts, 'form': form, 'message_up': message_up, 'message_down': message_down}
    print(backs)
    return render(request, 'main_page.html', context)

