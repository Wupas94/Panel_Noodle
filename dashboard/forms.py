from django import forms
from core.models import TimeEntry

class TimeEntryEditForm(forms.ModelForm):
    start_time = forms.DateTimeField(
        label='Czas rozpoczęcia',
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local'},
            format='%Y-%m-%dT%H:%M'
        )
    )
    end_time = forms.DateTimeField(
        label='Czas zakończenia',
        required=False,
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local'},
            format='%Y-%m-%dT%H:%M'
        )
    )
    notes = forms.CharField(
        label='Notatki',
        required=False,
        widget=forms.Textarea(attrs={'rows': 3})
    )

    class Meta:
        model = TimeEntry
        fields = ['start_time', 'end_time', 'notes']

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time and end_time <= start_time:
            raise forms.ValidationError(
                'Czas zakończenia musi być późniejszy niż czas rozpoczęcia.'
            )

        return cleaned_data

class TimeEntryCreateForm(forms.ModelForm):
    """Formularz do tworzenia nowego wpisu czasu pracy."""
    start_time = forms.DateTimeField(
        label='Czas rozpoczęcia',
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local'},
            format='%Y-%m-%dT%H:%M'
        )
    )
    end_time = forms.DateTimeField(
        label='Czas zakończenia',
        required=False,
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local'},
            format='%Y-%m-%dT%H:%M'
        )
    )
    notes = forms.CharField(
        label='Notatki',
        required=False,
        widget=forms.Textarea(attrs={'rows': 3})
    )

    class Meta:
        model = TimeEntry
        fields = ['start_time', 'end_time', 'notes']

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time and end_time <= start_time:
            raise forms.ValidationError(
                'Czas zakończenia musi być późniejszy niż czas rozpoczęcia.'
            )

        return cleaned_data 