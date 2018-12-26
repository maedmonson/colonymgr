from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewYardForm
from .forms import NewColonyForm
from .forms import ColonyForm
from .forms import NewQueenForm
from .forms import EditQueenForm
from .forms import Queen_logForm
from .forms import Colony_logForm
from .forms import Display_Colony_logForm
from .models import Yard
from .models import Colony
from .models import Colony_log
from .models import Queen
from .models import Queen_log
from django.views.generic import UpdateView

from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
@login_required
def home(request):
    #yards = Yard.objects.filter(created_by_id=self.request.us)
    yards = Yard.objects.all()
    return render(request, 'home.html', {'yards' : yards})

def colonies(request, home_pk):
    yard = Yard.objects.get(pk= home_pk)
    colonies = Colony.objects.filter(yard = yard)
    return render(request, 'colonies.html', {'yard':yard, 'colonies': colonies})

def queens(request, pk):
    colony =  get_object_or_404(Colony,pk=pk)
    yard = get_object_or_404(Yard, pk = colony.yard.pk)
    queens =  Queen.objects.filter(colony = colony)
    return render(request, 'queens.html', {'yard': yard, 'colony': colony, 'queens': queens})

def colony_logs(request, pk):
    colony = Colony.objects.get(pk = pk)
    yard = Yard.objects.get(pk = colony.yard.pk)
    colony_logs =  Colony_log.objects.filter(colony = colony)
    return render(request, 'colony_logs.html', {'yard' : yard, 'colony': colony, 'colony_logs': colony_logs})

def display_colony_log(request, pk):
    colony_log = Colony_log.objects.get(pk=pk)
    colony = Colony.objects.get(pk = colony_log.colony.pk)
    yard = Yard.objects.get(pk = colony.yard.pk)
    form = Display_Colony_logForm(initial={'colony': colony}, instance= colony_log)
    return render(request, 'display_colony_log.html', {'form' : form,'yard': yard, 'colony':colony})



def queen_logs(request, pk):
    queen = Queen.objects.get(pk=pk)
    queen_logs =  get_object_or_404(Queen_log, queen_id = queen.pk )
    return render(request, 'queens.html', {'queen': queen, 'queen_logs': queen_logs})


def new_yard(request):
    user = User.objects.first()
    if request.method == 'POST':
        form = NewYardForm(request.POST)
        if form.is_valid():
            yard = form.save(commit=False)
            yard.created_by = request.user
            yard.save()

            return redirect('home')
    else:
        form = NewYardForm()
    return render(request, 'new_yard.html',{'form' : form })

def new_colony(request, yard_pk):

    yard = Yard.objects.get(pk=yard_pk)


    if request.method == 'POST':
        form = NewColonyForm(request.POST)

        if form.is_valid():

            yard = form.cleaned_data.get('yard')

            colony = form.save(commit=False)
            colony.created_by = request.user
            colony.save()

            return redirect('colonies', home_pk=yard.pk)


    else:
        form = NewColonyForm(yard = yard)

    return render(request, 'new_colony.html',{'form' : form, 'yard': yard})

def new_colony_log(request, pk):
    user = request.user

    colony = Colony.objects.get(pk=pk)
    yard = Yard.objects.get(pk=colony.yard.pk)

    if request.method == 'POST':
        form = Colony_logForm(request.POST)
        if form.is_valid():
            colony_log = form.save(commit=False)
            colony_log.created_by = request.user
            colony_log.save()

            return redirect('colony_logs', pk = pk)
        else:
            print(form.errors)


    else:

        form = Colony_logForm(initial={'colony': colony})


    return render(request, 'new_colony_log.html',{'form' : form, 'yard': yard, 'colony':colony })


def new_queen(request, colony_pk):

    if request.method == 'POST':
        form = NewQueenForm(request.POST)

        print(form.is_valid())

        if form.is_valid():
            queen = form.save(commit=False)
            queen.created_by = request.user
            queen.save()

            return redirect('colonies', colony_pk)
    else:
        colony = Colony.objects.get(pk = colony_pk)
        yard = Yard.objects.get(pk = colony.yard.pk)
        form = NewQueenForm()

    return render(request, 'new_queen.html',{'form' : form, 'yard': yard, 'colony': colony })



class YardUpdateView(UpdateView):
    model = Yard
    fields = ('name','description','phone' )
    template_name = 'edit_yard.html'
    pk_url_kwarg = 'yard_pk'
    context_object_name = 'yard'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.save()
        return redirect('home')

class ColonyUpdateView(UpdateView):
    model = Colony
    form_class = ColonyForm
    template_name = 'edit_colony.html'
    pk_url_kwarg = 'colony_pk'
    context_object_name = 'colony'

    def get_context_data(self, **kwargs):
        colony_pk = self.kwargs['colony_pk']

        print('ColonyUpdateView var colony_pk value {}', format(colony_pk))

        colony = Colony.objects.get(pk = colony_pk)
        context = super(ColonyUpdateView, self).get_context_data(**kwargs)
        context['yard'] = Yard.objects.get(pk=colony.yard.pk)
        return context


    def form_valid(self, form):

        yard = form.cleaned_data.get('yard')

        post = form.save(commit=False)
        post.save()
        return redirect('colonies', home_pk = yard.pk)

class QueenUpdateView(UpdateView):
    model = Queen
    form_class = EditQueenForm
    template_name = 'edit_queen.html'
    pk_url_kwarg = 'queen_pk'
    context_object_name = 'queen'

    def get_context_data(self, **kwargs):
        context = super(QueenUpdateView, self).get_context_data(**kwargs)

        queen = Queen.objects.get(pk = self.kwargs['queen_pk'])

        context['yard'] =  queen.colony.yard
        context['colony'] = queen.colony
        return context


    def form_valid(self, form):
        post = form.save(commit=False)
        post.save()
        return redirect('home')

class Queen_logUpdateView(UpdateView):
    model = Queen_log
    form_class = Queen_logForm
    #fields = ('yard','location','colony_type','start_at','end_at' )
    template_name = 'edit_queen_log.html'
    pk_url_kwarg = 'queen_log_pk'
    context_object_name = 'queen_log'


    def form_valid(self, form):
        post = form.save(commit=False)
        post.save()
        return redirect('home')