import handlers.index as index

routes = [
    # all requests to / are handled by Index class
    ('*', '/', index.Index,  'index'),
]