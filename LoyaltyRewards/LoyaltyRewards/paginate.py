from .constants import DEFAULT_LIMIT, DEFAULT_PAGE


def paginate(query, extract, limit=None, page=None):
    """
    Paginate a query. 'limit' and 'page' may be None, in which case they are
    defaulted to sensible values. Page indices start at zero.
    This returns a dictionary containing:

        limit - as passed or defaulted
        page - as passed or defaulted
        page_count - total number of pages
        total - total results available
        last_page - True if this is the last page of results.
        items - an array of up to 'limit' paginated results. Each entry in the
                list is the value returned by the 'extract' function, which is
                passed a single instance.
    """
    if limit is None:
        limit = DEFAULT_LIMIT
    if page is None:
        page = DEFAULT_PAGE

    try:
        total = query.count()
    except:
        total = len(query)
    lower_limit = page * limit
    upper_limit = min(total, lower_limit + limit)
    # upper_limit = lower_limit + limit
    iteration = 0

    items = []
    for item in query[lower_limit:upper_limit]:
        iteration = iteration + 1
        ext = extract(item)
        if ext is not None:
            items.append(ext)

    index_of_last = (lower_limit + iteration)

    return {
        'limit': limit,
        'page': page,
        'page_count': int((total - 1) / limit) + 1,
        'total': total,
        'last_page': total == upper_limit,
        'iteration': iteration,
        'items': items,
        'index_of_first': lower_limit,
        'index_of_last': index_of_last,
    }
