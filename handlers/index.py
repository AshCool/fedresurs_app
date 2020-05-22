from datetime import date, timedelta

import aiohttp_jinja2
from aiohttp import web
from asyncpg import Record

from api import search_for_messages_data
from handlers.database import insert, select
from miscellaneous.log import log
from miscellaneous.misc import redirect, result_to_json_file

# class for / view methods
class Index(web.View):

    @aiohttp_jinja2.template('index.html')
    async def get(self):
        print('/ get')
        # result field will be set by a successful POST
        # otherwise, it will not exists, so checking for KeyError
        try:
            if self.request.app['type'] == 'messages_data':
                return {'type': 'messages_data', 'data': self.request.app['result']}
            elif self.request.app['type'] == 'request_id':
                return {'type': 'request_id', 'data': self.request.app['result']}
            elif self.request.app['type'] == 'empty_messages_data':
                return {'type': 'empty_messages_data'}
        except KeyError:
            return {'type': 'request_id', 'data': ''}

    async def post(self):
        print('/ post')
        # collecting data from the page
        data = await self.request.post()

        if data['type'] == 'form_request':
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
                self.request.app['type'] = 'request_id'
                self.request.app['result'] = [res[0]['request_id']]
            else:
                await log('Request error')
                return web.Response(body='request_error')

        elif data['type'] == 'submit_request':
            # parsing collected data
            # there should be request id
            if not data['request_id']:
                return web.Response(body='request_id_absence_error')
            elif not data['request_id'].isdigit():
                return web.Response(body='request_id_type_error')

            await log('Got request with id=' + str(data['request_id']))
            res = await select('request', data['request_id'])
            if isinstance(res[0], Record):
                # transforming res into list of str values (w/o id)
                res = [str(item) for item in res[0].values()][1:]
                await log('Requested parameters: ' + str(res))
            else:
                await log('Request error')
                return web.Response(body='request_error')

            await log('Making request to API...')
            messages_data = await search_for_messages_data(res[0], res[1], res[2], res[3])
            await log('Request successfully made')
            if not messages_data:
                await log('Got no messages')
                self.request.app['type'] = 'empty_messages_data'
                self.request.app['result'] = ''
            else:
                file = await result_to_json_file(messages_data)
                await log('Results are saved to ' + file)
                self.request.app['type'] = 'messages_data'
                self.request.app['result'] = messages_data

        redirect(self.request, 'index')
