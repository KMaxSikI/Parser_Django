from django.shortcuts import render
from .models import Post, Product
from .forms import ParsForm
import requests
import locale


def home(request):
    posts = Post.objects.all()  # Получение всех постов
    return render(request, 'home.html', context={'posts': posts})


def parse_form(request):
    form = ParsForm()
    return render(request, 'parse_form.html', context={'form': form})


def parse_results(request):
    category = None

    if request.method == 'POST':
        search = request.POST.get('category')  # Получение категории товаров из формы
        url = f'https://search.wb.ru/exactmatch/ru/common/v4/search?TestGroup=pk2_alpha05&TestID=351&appType=1&curr=rub&dest=-1257786&' \
              f'query={search}&resultset=catalog&sort=popular&spp=26&suppressSpellcheck=false'
        category = search

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

        # Сохранение данных в базу данных
        for i, n, r, f, c, u in zip(Id_product, Name, Raiting, Feedback, Cost, Url_product):
            product, created = Product.objects.get_or_create(
                article=i,
                defaults={
                    'category': search,
                    'name': n,
                    'rating': r,
                    'review_count': f,
                    'price': f'{c} руб.',
                    'url': u
                }
            )

        # Получение обновленных данных из базы для отображения на странице
        parsed_data = Product.objects.all()
        return render(request, 'parse_results.html', context={'parsed_data': parsed_data, 'category': category})
    else:
        return render(request, 'parse_results.html', {'message': 'Данные отсутствуют. Вернитесь к форме и введите запрос.'})  # Если запрос не POST, просто отображаем страницу без данных


def posts(request, id):
    post = Post.objects.get(id=id)
    return render(request, 'posts.html', context={'post': post})