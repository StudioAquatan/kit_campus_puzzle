import json
from django.views.generic import TemplateView, ListView, DetailView
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from puzzle.mixin import LoginRequiredMixin
from puzzle.models import Puzzle
from .models import Rank
from .forms import HiddenPartsPositionForm


class ExamListView(LoginRequiredMixin, ListView):
    template_name = 'exam_list.html'
    model = Puzzle


class ExamView(LoginRequiredMixin, TemplateView):
    template_name = 'exam.html'

    def get_context_data(self, **kwargs):
        ctx = super(ExamView, self).get_context_data(**kwargs)
        puzzle_id = self.kwargs['puzzle_id']
        selected_puzzle = get_object_or_404(Puzzle, id=puzzle_id)
        ctx['puzzle'] = selected_puzzle
        ctx['form'] = HiddenPartsPositionForm(selected_puzzle)
        return ctx

    def post(self, request, *args, **kwargs):
        puzzle_id = self.kwargs['puzzle_id']
        selected_puzzle = get_object_or_404(Puzzle, id=puzzle_id)
        form = HiddenPartsPositionForm(selected_puzzle, request.POST)
        coordinates = []
        if form.is_valid():
            for i, parts in enumerate(selected_puzzle.parts.all()):
                x_key = 'parts-left{num}'.format(num=i)
                y_key = 'parts-top{num}'.format(num=i)
                coordinates.append([form.cleaned_data[x_key], form.cleaned_data[y_key]])
        else:
            return HttpResponseBadRequest()
        new_rank = Rank(
            user=request.user,
            puzzle=selected_puzzle,
            coordinates=json.dumps(coordinates),
        )
        new_rank.score = new_rank.calculate_score(coordinates)
        new_rank.save()
        return redirect('exam:result', pk=new_rank.pk)


class RankingView(TemplateView):
    template_name = 'ranking.html'

    def get_context_data(self, **kwargs):
        ctx = super(RankingView, self).get_context_data(**kwargs)
        rank_group = []
        for puzzle in Puzzle.objects.all():
            ranker = Rank.objects.filter(puzzle__name=puzzle.name).order_by('-score')[:5]
            rank_group.append(ranker)
        ctx['rank_group'] = rank_group
        return ctx


class ResultView(DetailView):
    model = Rank
    template_name = 'exam_result.html'
