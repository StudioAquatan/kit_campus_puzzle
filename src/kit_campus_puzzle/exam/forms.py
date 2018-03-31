from django.forms import forms, HiddenInput, FloatField
from puzzle.models import Puzzle


class HiddenPartsPositionForm(forms.Form):

    def __init__(self, parent_puzzle: Puzzle, *args, **kwargs):
        super(HiddenPartsPositionForm, self).__init__(*args, **kwargs)
        for i, parts in enumerate(parent_puzzle.parts.all()):
            self.fields['parts-left{num}'.format(num=i)] = FloatField(
                label=parts.name + '-left',
                initial=0.0,
                widget=HiddenInput(
                    attrs={
                        'class': 'no-spinners form-control',
                    },
                ),
                required=True
            )
            self.fields['parts-top{num}'.format(num=i)] = FloatField(
                label=parts.name + '-top',
                initial=0.0,
                widget=HiddenInput(
                    attrs={
                        'class': 'no-spinners form-control',
                    },
                ),
                required=True
            )
