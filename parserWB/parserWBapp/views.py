from django.shortcuts import render, HttpResponseRedirect
from .models import Post, Product
from .forms import ParsForm, PostForm
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.urls import reverse, reverse_lazy

import requests
import locale


class HomeListView(ListView):
    model = Post
    template_name = 'home.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts.html'


class PostCreateView(CreateView):
    form_class = PostForm
    model = Post
    success_url = reverse_lazy('parsing:home')
    template_name = 'create.html'


class ParseFormView(FormView):
    template_name = 'parse_form.html'
    form_class = ParsForm
    success_url = reverse_lazy('myapp:parse_results')

    def perform_parse(self, category):
        url = f'https://search.wb.ru/exactmatch/ru/common/v4/search?TestGroup=pk2_alpha05&TestID=351&appType=1&curr=rub&dest=-1257786&' \
              f'query={category}&resultset=catalog&sort=popular&spp=26&suppressSpellcheck=false'

        resp = requests.get(url)
        resp.encoding = 'utf-8'
        locale.setlocale(locale.LC_ALL, '')

        Id_product = [i['id'] for i in resp.json()['data']['products']]
        Name = [n['name'] for n in resp.json()['data']['products']]
        Raiting = [r['reviewRating'] for r in resp.json()['data']['products']]
        Feedback = [f['feedbacks'] for f in resp.json()['data']['products']]
        Cost = [locale.format_string('%d', c['salePriceU'] // 100, grouping=True) for c in
                resp.json()['data']['products']]
        Url_product = [f'https://www.wildberries.ru/catalog/{u}/detail.aspx?targetUrl=XS' for u in Id_product]

        for i, n, r, f, c, u in zip(Id_product, Name, Raiting, Feedback, Cost, Url_product):
            product, created = Product.objects.get_or_create(
                article=i,
                defaults={
                    'category': category,
                    'name': n,
                    'rating': r,
                    'review_count': f,
                    'price': f'{c} руб.',
                    'url': u
                }
            )

    def form_valid(self, form):
        category = form.cleaned_data['category']
        self.perform_parse(category)
        return HttpResponseRedirect(self.get_success_url(category=category))

    def get_success_url(self, **kwargs):
        url = reverse('parsing:parse_results')
        return f"{url}?category={kwargs.get('category', '')}"


class ParseResultsView(ListView):
    model = Product
    template_name = 'parse_results.html'
    context_object_name = 'parsed_data'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.request.GET.get('category', '')
        context['category'] = category
        return context