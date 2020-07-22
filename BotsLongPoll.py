import aiohttp
from accessify import private
import asyncio
from main import VkAPI

class BotsLongPoll(VkAPI):
    def __init__(self):
        self.request_lngp_str = ''
        self.server = ''
        self.key = ''
        self.ts = ''

    @private
    async def build_request(self, command : str, params : dict) -> str:
        parameters = ''.join([f'&{k}={v}' for k, v in params.items()])
        req = f"https://api.vk.com/method/{command}?v={self.version}&access_token={self.access_token}{parameters}"
        return req

    async def get_longpoll_attrs(self, group_id : str) -> None:
        request = await self.build_request("groups.getLongPollServer", { "group_id": group_id })
        async with aiohttp.ClientSession() as session:
            async with session.get(request) as response:
                q = await response.json()
                self.server = q['response']['server']
                self.key = q['response']['key']
                self.ts = q['response']['ts']
                await self.build_lngp_str()

        return None

    async def build_lngp_str(self):
        self.request_lngp_str = f"{self.server}?act=a_check&key={self.key}&ts={self.ts}&wait=25"
        return self.request_lngp_str

    def longpoll_request(self, types : list, non_stop : bool):

        def decorator(func):
            async def wrapper():
                await asyncio.sleep(1)
                while True:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(self.request_lngp_str) as response:
                            q = await response.json()
                            
                            self.ts = q['ts']
                            await self.build_lngp_str()
                            if q['updates'][0]['type'] not in types:
                                continue

                            else:
                                await func()
                                if non_stop == True:
                                    continue
                                else:
                                    break
            return wrapper
        return decorator