from django.forms import forms, FloatField, NumberInput
from .models import Puzzle


class PartsPositionForm(forms.Form):

    def __init__(self, parent_puzzle: Puzzle, *args, **kwargs):
        super(PartsPositionForm, self).__init__(*args, **kwargs)
        for i, parts in enumerate(parent_puzzle.parts.all()):
            self.fields['parts-left{num}'.format(num=i)] = FloatField(
                label=parts.name + '-left',
                initial=parts.x,
                widget=NumberInput(
                    attrs={
                        'class': 'no-spinners form-control',
                    },
                ),
                required=True
            )
            self.fields['parts-top{num}'.format(num=i)] = FloatField(
                label=parts.name + '-top',
                initial=parts.y,
                widget=NumberInput(
                    attrs={
                        'class': 'no-spinners form-control',
                    },
                ),
                required=True
            )
