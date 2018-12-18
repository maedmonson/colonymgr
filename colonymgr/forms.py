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
            'visited_at': DateInput(),
            'colony': forms.Select(attrs={'readonly':'readonly'}),

        }

class Display_Colony_logForm(forms.ModelForm):

    class Meta:
        model = Colony_log
        fields = ['colony','subject','description','visited_at']

        widgets = {
            'visited_at': DateInput(),
            'colony': forms.Select(attrs={'readonly':'readonly'}),
            'subject': forms.TextInput(attrs={'readonly':'readonly'}),
            'description': forms.Textarea(attrs={'readonly':'readonly'}),
            'visited_at': forms.TextInput(attrs={'readonly':'readonly'}),

        }


class NewQueenForm(forms.ModelForm):


    class Meta:
       model = Queen
       fields = ['yard', 'colony', 'queen_no', 'queen_color', 'cell_install_at','birth_at','laying_at']

       localized_fields = ('cell_install_at','birth_at','laying_at')

       widgets = {
           'cell_install_at': DateInput(),
           'birth_at': DateInput(),
           'laying_at': DateInput()

       }




class EditQueenForm(forms.ModelForm):

    class Meta:
       model = Queen
       fields = ['yard', 'colony', 'queen_no', 'queen_color', 'cell_install_at','birth_at','laying_at']

       widgets = {
           'cell_install_at': DateInput(),
           'birth_at': DateInput(),
           'laying_at': DateInput()

       }



class Queen_logForm(forms.ModelForm):

    class Meta:
       model = Queen_log
       fields = ['queen', 'subject', 'description']

       widgets = {

       }

