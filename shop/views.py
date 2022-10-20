from django.shortcuts import render

from .scraping import scraping, ScrapingError


def fill_database(request):
    if request.method == 'POST' and request.user.is_staff:
        try:
            scraping()
        except ScrapingError as err:
            print(str(err))
            return render(request, 'shop/fill-products.html', {'message': str(err),
                                                               'title': 'SCRAPING',
                                                               })

    return render(request, 'shop/fill-products.html', {'message': None,
                                                       'title': 'SCRAPING',
                                                       })
