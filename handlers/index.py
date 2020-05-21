from datetime import date, timedelta

import aiohttp_jinja2
from aiohttp import web
from asyncpg import Record

from handlers.database import insert
from miscellaneous.log import log


def redirect(request, route):
    url = request.app.router[route].url_for()
    raise web.HTTPFound(url)

# class for / view methods
class Index(web.View):

    @aiohttp_jinja2.template('index.html')
    async def get(self):
        print('/ get')
        # result field will be set by a successful POST
        # otherwise, it will not exists, so checking for KeyError
        try:
            return {'data': self.request.app['result']}
        except KeyError:
            return {'data': ['']}

    async def post(self):
        print('/ post')
        # collecting data from the page
        data = await self.request.post()

        # parsing collected data
        # there should be begin date
        if not data['begin']:
            return web.Response(body='begin_date_error')
        begin = date(*[int(x) for x in data['begin'].split('-')])
        # if there's no end date, set it so date span will be max (30 days)
        if not data['end']:
            end = begin + timedelta(days=30)
        else:
            end = date(*[int(x) for x in data['end'].split('-')])

        delta = end - begin
        # end date should be later than begin one, but no more than 30 days ('cause of API)
        if delta.days > 30:
            return web.Response(body='date_span_error')
        elif delta.days < 0:
            return web.Response(body='end_date_error')

        # if participant type is specified, id should be provided
        if data['participant_type'] != 'any' and not data['participant_id']:
            return web.Response(body='participant_id_error')
        # inserting values into DB
        # returning value is a inserted row
        await log('Got request with following parameters: begin_date=' + str(begin) + ', end_date=' + str(end) +
                  ', participant_type=' + str(data['participant_type']) +
                  ', participant_id=' + str(data['participant_id']))
        res = await insert('request', begin_date=str(begin), end_date=str(end),
                                            participant_type=data['participant_type'],
                                            participant_id=data['participant_id'])
        # if returned value is a correct row, display it
        if isinstance(res[0], Record):
            await log('Request id=' + str(res[0]['request_id']))
            self.request.app['result'] = [res[0]['request_id']]

        redirect(self.request, 'index')


