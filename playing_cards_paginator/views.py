from django.shortcuts import redirect, render
from .models import BackFile, FrontFiles
from .forms import DeckForm
from django.conf import settings


def file_loader(request):
    message = 'Upload as many files as you want!'
    # Handle file upload
    if request.method == 'POST':
        form = DeckForm(request.POST, request.FILES)
        if form.is_valid():
            group_name = request.POST['name']
            newdoc = BackFile(back=request.FILES['back'], group_name=group_name)
            newdoc.save()

            for front in request.FILES.getlist('fronts'):
                newdoc = FrontFiles(front=front, group_name=group_name)
                newdoc.save()


            # Redirect to the document list after POST
            return redirect('file_loader')
        else:
            message = 'The form is not valid. Fix the following error:'
    else:
        form = DeckForm()  # An empty, unbound form

    # Load documents for the list page
    documents = BackFile.objects.all()

    # Render list page with the documents and the form
    context = {'documents': documents, 'form': form, 'message': message}
    return render(request, 'list.html', context)

