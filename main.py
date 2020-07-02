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
            raise AttributeError ("'user_id' is not in params")
        
        elif "type" not in params:
            raise AttributeError ("'type' is not in params")
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
            raise AttributeError ("'group_id' is not in params")
        elif "title" not in params:
            raise AttributeError ("'title' is not in params")
        elif "address" not in params:
            raise AttributeError ("'address' is not in params")
        elif "country_id" not in params:
            raise AttributeError ("'country_id' is not in params")
        elif "city_id" not in params:
            raise AttributeError ("'city_id' is not in params")
        elif "latitude" not in params:
            raise AttributeError ("'latitude' is not in params")
        elif "longitude" not in params:
            raise AttributeError ("'longitude' is not in params")
    
        str_req = await self.build_request("groups.addAddress", params)
        response = await self.send_request_get_dict(str_req)
        return response

    async def group_add_callback(self, params : dict) -> dict:
        if "group_id" not in params:
            raise AttributeError ("'group_id' is not in params")
        elif "url" not in params:
            raise AttributeError ("'url' is not in params")
        elif "title" not in params:
            raise AttributeError ("'title' is not in params")
        str_req = await self.build_request("groups.addCallbackServer", params)
        response = await self.send_request_get_dict(str_req)
        return response

    async def group_add_link(self, params : dict) -> dict:
        if "group_id" not in params:
            raise AttributeError ("'group_id' is not in params")
        elif "link" not in params:
            raise AttributeError ("'link' is not in params")
        str_req = await self.build_request("groups.addLink", params)
        response = await self.send_request_get_dict(str_req)
        return response

    async def group_approve_request(self, params : dict) -> dict:
        if "group_id" not in params:
            raise AttributeError ("'group_id' is not in params")
        elif "user_id" not in params:
            raise AttributeError ("'user_id' is not in params")
        str_req = await self.build_request("groups.approveRequest", params)
        response = await self.send_request_get_dict(str_req)
        return response

    async def group_ban(self, params : dict) -> bool:
        if "group_id" not in params:
            raise AttributeError ("'group_id' is not in params")
        str_req = await self.build_request("groups.ban", params)
        response = await self.send_request_get_dict(str_req)
        return bool(response)

    async def group_create(self, params : dict) -> dict:
        if "title" not in params:
            raise AttributeError("'title' not in params")
        str_req = await self.build_request("groups.create", params)
        response = await self.send_request_get_dict(str_req)
        return response

    async def group_delete_address(self, params : dict) -> dict:
        if "group_id" not in params:
            raise AttributeError ("'group_id' is not in params")
        elif "address_id" not in params:
            raise AttributeError ("'address_id' is not in params")
    
        str_req = await self.build_request("groups.deleteAddress", params)
        response = await self.send_request_get_dict(str_req)
        return response

    async def group_delete_callback(self, params : dict) -> dict:
        if "group_id" not in params:
            raise AttributeError ("'group_id' is not in params")
        elif "server_id" not in params:
            raise AttributeError ("'server_id' is not in params")
        str_req = await self.build_request("groups.deleteCallbackServer", params)
        response = await self.send_request_get_dict(str_req)
        return response

    async def group_delete_link(self, params : dict) -> dict:
        if "group_id" not in params:
            raise AttributeError ("'group_id' is not in params")
        elif "link_id" not in params:
            raise AttributeError ("'link_id' is not in params")
        str_req = await self.build_request("groups.deleteLink", params)
        response = await self.send_request_get_dict(str_req)
        return response

    async def group_disable_online(self, params : dict) -> bool:
        if "group_id" not in params:
            raise AttributeError ("'group_id' is not in params")
        str_req = await self.build_request("groups.disableOnline", params)
        response = await self.send_request_get_dict(str_req)
        return bool(response)

    async def group_edit(self, params : dict) -> bool:
        if "group_id" not in params:
            raise AttributeError ("'group_id' is not in params")
        str_req = await self.build_request("groups.edit", params)
        response = await self.send_request_get_dict(str_req)
        return bool(response)

    async def group_edit_address(self, params : dict) -> dict:
        if "group_id" not in params:
            raise AttributeError ("'group_id' is not in params")
        elif "address_id" not in params:
            raise AttributeError ("'address_id' is not in params")
    
        str_req = await self.build_request("groups.editAddress", params)
        response = await self.send_request_get_dict(str_req)
        return response