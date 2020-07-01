import json
import aiohttp
from accessify import private

class VkAPI:
    def __init__(self, access_token : str, version : str):
        self.access_token = access_token
        self.version = version

    @private
    async def build_request(self, command : str, params : dict) -> str:
        parameters = ''.join([f'&{k}={v}' for k, v in params.items()])
        req = f"https://api.vk.com/method/{command}?v={self.version}&access_token={self.access_token}{parameters}"
        return req

    @private
    async def send_request_get_dict(self, string_request : str):
        async with aiohttp.ClientSession() as session:
            async with session.get(string_request) as response:
                q = await response.json()

        return q['response']

    """
        USER COMMANDS
    """
    async def get_user(self, params : dict, user_id=None) -> dict:
        if user_id != None:
            str_req = await self.build_request("users.get", {'user_ids': user_id}.update(params))
        else: 
            str_req = await self.build_request("users.get", { })

        user = await self.send_request_get_dict(str_req)
        for lst in user:
            user = lst

        return user

    async def get_user_subscriptions(self, params : dict) -> list:
        str_req = await self.build_request("users.getSubscriptions", params)
        response = (await self.send_request_get_dict(str_req))['items']
        names = []
        for subscription in response:
            names.append(subscription['name'])
        return names

    async def user_report(self, params : dict) -> bool:
        if "user_id" not in params:
            raise ValueError("'user_id' is not in params")
        
        if "type" not in params:
            raise ValueError("'type' is not in params")
        str_req = await self.build_request("users.report", params)
        code = await self.send_request_get_dict(str_req)
        return bool(code)

    async def get_user_followers(self, params : dict) -> dict:
        str_req = await self.build_request("users.getFollowers", params)
        response = (await self.send_request_get_dict(str_req))['items']
        return response

    async def user_search(self, params : dict) -> dict:
        str_req = await self.build_request("users.search", params)
        response = (await self.send_request_get_dict(str_req))['items']
        return response

    """
            GROUP COMMANDS
    """
    async def get_user_groups(self, params : dict, get_names = False) -> list:
        str_req = await self.build_request("groups.get", params)
        response = await self.send_request_get_dict(str_req)
        groups = []

        if get_names == True:
            groups_response = response['items']
            for group in groups_response:
                groups.append(group['name'])
        else:
            groups = response['items']

        return groups 

    async def group_add_address(self, params : dict) -> dict:
        if "group_id" not in params:
            raise ValueError("'group_id' is not in params")
        if "title" not in params:
            raise ValueError("'title' is not in params")
        if "address" not in params:
            raise ValueError("'address' is not in params")
        if "country_id" not in params:
            raise ValueError("'country_id' is not in params")
        if "city_id" not in params:
            raise ValueError("'city_id' is not in params")
        if "latitude" not in params:
            raise ValueError("'latitude' is not in params")
        if "longitude" not in params:
            raise ValueError("'longitude' is not in params")
    
        str_req = await self.build_request("groups.addAddress", params)
        response = await self.send_request_get_dict(str_req)
        return response

    async def group_add_callback(self, params : dict) -> dict:
        if "group_id" not in params:
            raise ValueError("'group_id' is not in params")
        if "url" not in params:
            raise ValueError("'url' is not in params")
        if "title" not in params:
            raise ValueError("'title' is not in params")
        str_req = await self.build_request("groups.addCallbackServer", params)
        response = await self.send_request_get_dict(str_req)
        return response