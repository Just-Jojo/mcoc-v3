import aiohttp
import typing


URL = "https://raw.githubusercontent.com/CollectorDevTeam/assets/master/data/images/maps/catmurdock/SQ/{map}.png"


async def get_map(quest: str) -> typing.Union[str, None]:
    if quest.split(".")[1:] > [1, 6] or quest.split('.')[1:] < [1, 1]:
        return None
    quest = f"sq_{quest}"
    async with aiohttp.ClientSession() as session:
        async with session.get((url := URL.format(map=quest))) as response:
            if response.status == 200:
                ret = url
            else:
                ret = None
    return ret
