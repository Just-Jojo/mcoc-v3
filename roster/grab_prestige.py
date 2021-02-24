import aiohttp
import typing
import json


URL = "https://raw.githubusercontent.com/CollectorDevTeam/assets/master/data/json/backup_prestige.json"


async def transfer_keys(data: typing.List[dict], look_for: str):
    for item in data:
        key = item.pop("mattkraftid")
        if key == look_for:
            return item
    return "ERROR"


async def grab_prestige(champion: str, sig: str) -> str:
    if not sig.startswith("sig"):
        sig = f"sig{sig}"
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            data = json.loads(await response.text())
    if data is None:
        return "ERROR"
    else:
        grabber = data["rows"]
        data = await transfer_keys(grabber, look_for=champion)
        if data == "ERROR":
            return data
        else:
            return data[sig]
