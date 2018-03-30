from django.views.generic import TemplateView, ListView
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseBadRequest
from .mixin import LoginRequiredMixin, StaffRequiredMixin
from .models import Puzzle
from .forms import PartsPositionForm


class PuzzleView(LoginRequiredMixin, TemplateView):
    template_name = 'puzzle.html'

    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(**kwargs)
        puzzle_id = self.kwargs['puzzle_id']
        selected_puzzle = get_object_or_404(Puzzle, id=puzzle_id)
        ctx['puzzle'] = selected_puzzle
        return self.render_to_response(ctx)


class PuzzleListView(StaffRequiredMixin, ListView):
    paginate_by = 5
    model = Puzzle
    template_name = 'puzzle_list.html'


class PuzzleEditView(StaffRequiredMixin, TemplateView):
    template_name = 'create_puzzle.html'

    def get_context_data(self, **kwargs):
        ctx = super(PuzzleEditView, self).get_context_data(**kwargs)
        puzzle_id = self.kwargs['puzzle_id']
        selected_puzzle = get_object_or_404(Puzzle, id=puzzle_id)
        ctx['puzzle'] = selected_puzzle
        ctx['form'] = PartsPositionForm(parent_puzzle=selected_puzzle)
        return ctx

    def post(self, request, *args, **kwargs):
        puzzle_id = self.kwargs['puzzle_id']
        selected_puzzle = get_object_or_404(Puzzle, id=puzzle_id)
        form = PartsPositionForm(selected_puzzle, request.POST)
        if form.is_valid():
            for i, parts in enumerate(selected_puzzle.parts.all()):
                x_key = 'parts-left{num}'.format(num=i)
                y_key = 'parts-top{num}'.format(num=i)
                parts.x = form.cleaned_data[x_key]
                parts.y = form.cleaned_data[y_key]
                parts.save()
            selected_puzzle.save()
        else:
            return HttpResponseBadRequest()
        return redirect('puzzle:list')
