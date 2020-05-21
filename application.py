import aiohttp_jinja2
import jinja2

from aiohttp import web
from os import environ

from routes import routes


# initializing app
app = web.Application()
# appending templates
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
# adding routes from routes.py to route table
for route in routes:
    app.router.add_route(route[0], route[1], route[2], name=route[3])
# adding routes to static content
app.add_routes([web.static('/static', 'static')])

PORT = environ.get('PORT', 5000)

# TODO: logging
print('Starting app...')
web.run_app(app, port=PORT)
print('Shutting down...')