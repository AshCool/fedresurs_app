from aiohttp import web

# checks if s is in date format (YYYY-MM-DD)
def isdate(s):
    for c in s:
        if c != '-' and not c.isdigit():
            return False
    return True

# redirects request to a given route
def redirect(request, route):
    url = request.app.router[route].url_for()
    raise web.HTTPFound(url)