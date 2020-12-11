# coding: utf-8

from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic import DeleteView
from django.views.generic import FormView
from django.views.generic import UpdateView
from django.views.generic.base import TemplateView, RedirectView

from main.forms import AddForm
from main.models import Chain, WordBlock, Word, Tag


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        return super(HomeView, self).get_context_data(**kwargs)


class AddView(FormView):
    template_name = 'add.html'
    form_class = AddForm
    success_url = reverse_lazy('add')

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AddView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(AddView, self).get_context_data(**kwargs)

    def form_invalid(self, form):
        return super(AddView, self).form_invalid(form)

    def form_valid(self, form):
        blocks = {
            'ru': WordBlock.objects.create(),
            'en': WordBlock.objects.create(),
            'de': WordBlock.objects.create(),
        }

        for lang, block in blocks.items():
            for i in range(1, 4):
                value = form.cleaned_data.get('%s_value%s' % (lang, i))
                info = form.cleaned_data.get('%s_info%s' % (lang, i))
                if value:
                    Word.objects.create(
                        value=value,
                        info=info,
                        order=i,
                        lang=lang,
                        block=block,
                    )

        tag_name = form.cleaned_data.get('tag')
        tag, created = Tag.objects.get_or_create(name=tag_name)
        if created:
            tag.color = Tag.get_random_color()
            tag.save()

        Chain.objects.create(
            ru_block=blocks['ru'],
            en_block=blocks['en'],
            de_block=blocks['de'],
            part_speech=form.cleaned_data.get('part_speech'),
            tag=tag,
        )

        return super(AddView, self).form_valid(form)


class EditView(UpdateView):
    template_name = 'edit.html'
    form_class = AddForm
    success_url = reverse_lazy('show')

    def get_object(self, queryset=None):
        return get_object_or_404(Chain, pk=self.kwargs.get('pk'))

    def form_valid(self, form):
        self.object = self.get_object()  # chain

        self.object.ru_block.words.all().delete()
        self.object.en_block.words.all().delete()
        self.object.de_block.words.all().delete()

        blocks = {
            'ru': self.object.ru_block,
            'en': self.object.en_block,
            'de': self.object.de_block,
        }

        for lang, block in blocks.items():
            for i in range(1, 4):
                value = form.cleaned_data.get('%s_value%s' % (lang, i))
                info = form.cleaned_data.get('%s_info%s' % (lang, i))
                if value:
                    Word.objects.create(
                        value=value,
                        info=info,
                        order=i,
                        lang=lang,
                        block=block,
                    )

        tag_name = form.cleaned_data.get('tag')
        tag, created = Tag.objects.get_or_create(name=tag_name)
        if created:
            tag.color = Tag.get_random_color()
            tag.save()

        self.object.tag = tag
        self.object.part_speech = form.cleaned_data.get('part_speech')
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class ShowView(TemplateView):
    template_name = 'show.html'

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ShowView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        chains = Chain.objects.prefetch_related(
            'ru_block', 'en_block', 'de_block',
            'ru_block__words', 'en_block__words', 'de_block__words',
            'tag',
        )

        if self.request.method == 'POST':
            s = self.request.POST.get('search')
            if s:
                chains = filter(lambda x: x.contains(s), chains)

        o = self.request.GET.get('o')
        if o:
            if o == "name":
                chains = sorted(chains, key=lambda x: x.ru_block.words.get(order=1).value)
            if o == "tag":
                chains = sorted(chains, key=lambda x: x.tag.name)
            if o == "part_speech":
                chains = chains.order_by('part_speech')

        context = super(ShowView, self).get_context_data(**kwargs)
        context.update({
            'chains': chains,
        })

        return context

    def post(self, request):
        return render(request, self.template_name, self.get_context_data())


class SomeDeleteView(DeleteView):
    template_name = "confirm.html"
    model = Chain
    success_url = reverse_lazy('show')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()  # chain

        self.object.ru_block.words.all().delete()
        self.object.en_block.words.all().delete()
        self.object.de_block.words.all().delete()

        self.object.ru_block.delete()
        self.object.en_block.delete()
        self.object.de_block.delete()

        self.object.delete()

        return HttpResponseRedirect(self.get_success_url())


class SomeRedirectView(RedirectView):
    url = reverse_lazy('home')
    permanent = False

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SomeRedirectView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(SomeRedirectView, self).get(request, *args, **kwargs)


class SomeListView(generic.ListView):
    template_name = 'home.html'

    def get_queryset(self):
        return Chain.objects.order_by("created_at").reverse()[:5]


class SomeDetailView(generic.DetailView):
    model = Chain
    template_name = 'detail.html'
