from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewYardForm
from .forms import DeleteYardForm
from .forms import NewColonyForm
from .forms import ColonyForm
from .forms import NewQueenForm
from .forms import EditQueenForm
from .forms import DeleteQueenForm
from .forms import Queen_logForm
from .forms import Colony_logForm
from .forms import Display_Colony_logForm
from .models import Yard
from .models import Colony
from .models import Colony_log
from .models import Queen
from .models import Queen_log
from django.views.generic import UpdateView
from django.views.generic import DeleteView

from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
@login_required
def home(request):
    #yards = Yard.objects.filter(created_by_id=self.request.us)
    yards = Yard.objects.all().order_by('name')
    return render(request, 'home.html', {'yards' : yards})

def colonies(request, home_pk):
    yard = Yard.objects.get(pk= home_pk)
    colonies = Colony.objects.filter(yard = yard).order_by('location')
    return render(request, 'colonies.html', {'yard':yard, 'colonies': colonies})

def queens(request, pk):
    colony =  Colony.objects.get(pk=pk)
    yard =  Yard.objects.get(pk = colony.yard.pk)
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

    colony = Colony.objects.get(pk=colony_pk)
    yard = Yard.objects.get(pk=colony.yard.pk)

    if request.method == 'POST':
        form = NewQueenForm(request.POST)


        if form.is_valid():
            queen = form.save(commit=False)
            queen.created_by = request.user
            queen.save()

            return redirect('queens', colony_pk)
        else:
            print(form.errors)
    else:
        form = NewQueenForm(initial={'colony': colony, 'yard' : yard})

    return render(request, 'new_queen.html',{'form' : form, 'yard': yard, 'colony': colony })


def delete_queen(request, queen_pk):

    queen = Queen.objects.get(pk=queen_pk)
    colony = Colony.objects.get(pk = queen.colony.pk)
    yard = Yard.objects.get(pk = colony.yard.pk)

    if request.method == 'POST':
        form = DeleteQueenForm(request.POST)


        if form.is_valid():
            queen.delete()

            return redirect('queens', colony.pk)
        else:
            print(form.errors)
    else:

        print('--------')
        print(queen_pk)

        context = {

            'queen' : queen,
            'colony' : colony,
            'yard' : yard


        }

        form = DeleteQueenForm()


    return render(request, 'delete_queen.html',{'form' : form, 'queen': queen, 'colony' : colony, 'yard': yard  }, context)



def load_colonies(request):
    pk = request.GET.get('pk')
    colonies = Colony.objects.filter(pk = pk)
    return render(request, 'queen/colony_dropdown_list_options.html', {'colonies': colonies})



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


class YardDeleteView(UpdateView):
    model = Yard
    form_class = DeleteYardForm
    template_name = 'delete_yard.html'
    pk_url_kwarg = 'yard_pk'
    context_object_name = 'yard'

    def get_context_data(self, **kwargs):
        context = super(YardDeleteView, self).get_context_data(**kwargs)

        yard = Yard.objects.get(pk = self.kwargs['yard_pk'])

        context['yard'] =  yard

        return context


    def form_valid(self, form):

        yard = form.cleaned_data.get('yard')

        post = form.save(commit=False)
        post.delete()
        return redirect('home')

    def get_form_kwargs(self):
        kwargs = super(YardDeleteView, self).get_form_kwargs()
        kwargs['yard_pk'] = self.kwargs['yard_pk']
        return kwargs



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

class Colony_logUpdateView(UpdateView):
    model = Colony_log
    form_class = Colony_logForm
    template_name = 'edit_colony_log.html'
    pk_url_kwarg = 'colony_log_pk'
    context_object_name = 'colony_log'

    def get_context_data(self, **kwargs):
        colony_log_pk = self.kwargs['colony_log_pk']

        colony_log = Colony_log.objects.get(pk = colony_log_pk)
        colony = Colony.objects.get(pk = colony_log.colony.pk)
        yard = Yard.objects.get(pk = colony.yard.pk)
        context = super(Colony_logUpdateView, self).get_context_data(**kwargs)
        context['yard'] = yard
        context['colony'] = colony
        return context


    def form_valid(self, form):

        colony = form.cleaned_data.get('colony')

        post = form.save(commit=False)
        post.save()
        return redirect('colony_logs', pk = colony.pk)


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

        colony = form.cleaned_data.get('colony')

        post = form.save(commit=False)
        post.save()
        return redirect('queens', pk=colony.pk)

    def get_form_kwargs(self):
        kwargs = super(QueenUpdateView, self).get_form_kwargs()
        kwargs['queen_pk'] = self.kwargs['queen_pk']
        return kwargs


class QueenDeleteView(UpdateView):
    model = Queen
    form_class = DeleteQueenForm
    template_name = 'delete_queen.html'
    pk_url_kwarg = 'queen_pk'
    context_object_name = 'queen'

    def get_context_data(self, **kwargs):
        context = super(QueenDeleteView, self).get_context_data(**kwargs)

        queen = Queen.objects.get(pk = self.kwargs['queen_pk'])

        context['yard'] =  queen.colony.yard
        context['colony'] = queen.colony
        return context


    def form_valid(self, form):

        colony = form.cleaned_data.get('colony')

        post = form.save(commit=False)
        post.delete()
        return redirect('queens', pk=colony.pk)

    def get_form_kwargs(self):
        kwargs = super(QueenDeleteView, self).get_form_kwargs()
        kwargs['queen_pk'] = self.kwargs['queen_pk']
        return kwargs



class Queen_UpdateYard(UpdateView):
    model = Queen
    form_class = EditQueenForm
    template_name = 'edit_queen.html'
    pk_url_kwarg = 'queen_pk'
    context_object_name = 'queen'

    def get_context_data(self, **kwargs):
        context = super(QueenUpdateView, self).get_context_data(**kwargs)

        queen = Queen.objects.get(pk=self.kwargs['queen_pk'])

        context['yard'] = queen.colony.yard
        context['colony'] = queen.colony
        return context

    def form_valid(self, form):
        colony = form.cleaned_data.get('colony')

        post = form.save(commit=False)
        post.save()
        return redirect('queens', pk=colony.pk)

    def get_form_kwargs(self):
        kwargs = super(QueenUpdateView, self).get_form_kwargs()
        kwargs['queen_pk'] = self.kwargs['queen_pk']
        return kwargs


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