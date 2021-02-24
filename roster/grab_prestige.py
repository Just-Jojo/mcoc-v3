import aiohttp
import typing
import json
import logging


log = logging.getLogger("red.mcoc-v3/jojo.prestigegrab")

URL = "https://raw.githubusercontent.com/CollectorDevTeam/assets/master/data/json/backup_prestige.json"
IMAGE_URL = "https://raw.githubusercontent.com/CollectorDevTeam/assets/master/data/images/{champion}.png"


async def transfer_keys(data: typing.List[dict], look_for: str):
    for item in data:
        key = item.pop("mattkraftid")
        if key == look_for:
            return item
    return "ERROR"


async def grab_prestige(
    champion: str, sig: str
) -> typing.Tuple[str, typing.Union[None, str]]:
    if not sig.startswith("sig"):
        sig = f"sig{sig}"
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            data = json.loads(await response.text())
        async with session.get(
            (url := IMAGE_URL.format(champion=champion))
        ) as response:
            log.info(response.status, url)
            if response.status == 200:
                thumbnail = url
            else:
                thumbnail = None
    if data is None:
        return "ERROR", None
    else:
        grabber = data["rows"]
        data = await transfer_keys(grabber, look_for=champion)
        if data == "ERROR":
            return data, None
        else:
            return data[sig], thumbnail
