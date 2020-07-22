import aiohttp
from accessify import private
import asyncio

class BotsLongPoll():
    def __init__(self):
        self.request_lngp_str = ''
        self.server = ''
        self.key = ''
        self.ts = ''

    async def write_longpoll_attrs(self, server, key, ts) -> None:
        self.server = server
        self.key = key
        self.ts = ts
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

                            if q['updates'] == [] or q['updates'][0]['type'] not in types:
                                continue
                            else:
                                await func()
                                if non_stop == True:
                                    continue
                                else:
                                    break
            return wrapper
        return decorator