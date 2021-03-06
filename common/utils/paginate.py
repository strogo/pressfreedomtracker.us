from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


DEFAULT_PAGE_KEY = 'page'


def paginate(request, items, page_key=DEFAULT_PAGE_KEY, per_page=20, orphans=10):
    try:
        page_number = int(request.GET.get(page_key, 1))
        endpage = int(request.GET.get('endpage', 1))
    except ValueError:
        page_number = 1
        endpage = 1

    # See https://docs.djangoproject.com/en/1.10/topics/pagination/#using-paginator-in-a-view
    paginator = Paginator(items, per_page)
    try:
        page = paginator.page(page_number)
        if endpage > page_number and page_number == 1:
            per_page = endpage * per_page
            page = Paginator(items, per_page).page(1)
        elif endpage >= page_number and endpage != 1:
            page = paginator.page(endpage + 1)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return paginator, page
