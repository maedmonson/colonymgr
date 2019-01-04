from django import forms
from  .models import Yard
from  .models import Colony
from  .models import Colony_log
from  .models import Queen
from  .models import Queen_log
from datetimepicker.widgets import DateTimePicker


COLONY_TYPES = [('queen_nuk','Queen Nuk'),('2_frame','2 Frame'),('3_frame','3 Fames'),('5_frame','5 Frames'),('8_frame','8 Frames'),('10_frame','10 Frames')]


class NewYardForm(forms.ModelForm):

    class Meta:
       model = Yard
       fields = ['name', 'description','phone']


class DateInput(forms.DateInput):
    input_type = 'date'


class NewColonyForm(forms.ModelForm):

    class Meta:
        model = Colony
        fields = ['yard','colony_type','location','start_at','end_at']

        widgets = {
            'start_at': DateInput(),
            'end_at': DateInput(),
            'yard': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.yard = kwargs.pop('yard', None)

        super(NewColonyForm, self).__init__(*args, **kwargs)

        self.fields['yard'].empty_label = None
        self.fields['yard'].initial =  self.yard


    colony_type = forms.CharField(label='Colony Type?', widget=forms.Select(choices=COLONY_TYPES))







class ColonyForm(forms.ModelForm):

    class Meta:
        model = Colony
        fields = ['yard','colony_type','location','start_at','end_at']

        widgets = {
            'start_at': DateInput(),
            'end_at': DateInput(),
        }




    def __init__(self, *args, **kwargs):

        colony_pk = kwargs.pop("colony_pk", None)



        super(ColonyForm, self).__init__(*args, **kwargs)

        #colony = Colony.objects.get(pk = colony_pk)

        print('colony_pk',colony_pk)


        #self.fields['yard'].queryset = Yard.objects.all()
        self.fields['yard'].empty_label = None
        #self.fields['yard'].initial = Yard.objects.filter(pk = colony.yard.pk)

    colony_type = forms.CharField(label='Colony Type?', widget=forms.Select(choices=COLONY_TYPES))

class Colony_logForm(forms.ModelForm):

    class Meta:
        model = Colony_log
        fields = ['colony','subject','description','visited_at']
        widgets = {
                   'visited_at': DateInput()

                    }


class Display_Colony_logForm(forms.ModelForm):

    class Meta:
        model = Colony_log
        fields = ['colony','subject','description','visited_at']

        widgets = {
            'colony': forms.HiddenInput(),
            'visited_at': DateInput(),
            'subject': forms.TextInput(attrs={'readonly':'readonly'}),
            'description': forms.Textarea(attrs={'readonly':'readonly'}),
            'visited_at': forms.TextInput(attrs={'readonly':'readonly'}),

        }


class NewQueenForm(forms.ModelForm):


    class Meta:
       model = Queen
       fields = ['yard', 'colony', 'queen_no', 'queen_color', 'cell_install_at','birth_at','laying_at']

       widgets = {
           'yard': forms.HiddenInput(),
           'colony': forms.HiddenInput(),
           'cell_install_at':DateInput(),
           'birth_at': DateInput(),
           'laying_at': DateInput()
       }




class EditQueenForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        queen_pk = kwargs.pop('queen_pk')

        super(EditQueenForm, self).__init__(*args, **kwargs)
        queen = Queen.objects.get(pk=queen_pk)

        self.fields['queen_no'].label = 'Queen Tag No:'
        self.fields['queen_color'].label = 'Queen Tag Color:'

        self.fields['yard'].empty_label = None

        self.fields['colony'].empty_label = None
        self.fields['colony'].queryset = Colony.objects.filter(yard=queen.yard)

        if 'yard' in self.data:
            try:
                yard_id = int(self.data.get('yard'))
                self.fields['colony'].queryset = Colony.objects.filter(yard_id=yard_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['colony'].queryset = Colony.objects.filter(yard_id = self.instance.yard.pk)

    class Meta:
        model = Queen
        fields = ['yard','colony', 'queen_no', 'queen_color', 'cell_install_at','birth_at','laying_at']

        widgets = {
            'cell_install_at': DateInput(),
            'birth_at': DateInput(),
            'laying_at': DateInput()
        }

class DeleteQueenForm(forms.ModelForm):


    def __init__(self, *args, **kwargs):

        print('---- __init___DeleteQueenForm')

        queen_pk = kwargs.pop('queen_pk')

        print(queen_pk)

        super(DeleteQueenForm, self).__init__(*args, **kwargs)
        queen = Queen.objects.get(pk=queen_pk)

        self.fields['queen_no'].label = 'Queen Tag No:'
        self.fields['queen_color'].label = 'Queen Tag Color:'

        self.fields['yard'].empty_label = None

        self.fields['colony'].empty_label = None
        self.fields['colony'].queryset = Colony.objects.filter(yard=queen.yard)

        if 'yard' in self.data:
            try:
                yard_id = int(self.data.get('yard'))
                self.fields['colony'].queryset = Colony.objects.filter(yard_id=yard_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['colony'].queryset = Colony.objects.filter(yard_id = self.instance.yard.pk)

    class Meta:
       model = Queen
       fields = ['yard', 'colony', 'queen_no', 'queen_color', 'cell_install_at','birth_at','laying_at']

       widgets = {
           'yard': forms.HiddenInput(),
           'colony': forms.HiddenInput(),
           'cell_install_at':DateInput(),
           'birth_at': DateInput(),
           'laying_at': DateInput()
       }







class Queen_logForm(forms.ModelForm):

    class Meta:
       model = Queen_log
       fields = ['queen', 'subject', 'description']

       widgets = {

       }

