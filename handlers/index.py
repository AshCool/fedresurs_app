from aiohttp import web
import aiohttp_jinja2
import time

def redirect(request, route):
    url = request.app.router[route].url_for()
    raise web.HTTPFound(url)

# class for / view methods
class Index(web.View):

    @aiohttp_jinja2.template('index.html')
    async def get(self):
        # TODO: logging
        print('/ get')
        print(await self.request.text())
        return None

    async def post(self):
        print('/ post')
        data = await self.request.post()
        print('time', time.time(), 'data', data)
        if not True:
            return web.Response(body='error')
        else:
            redirect(self.request, 'index')


