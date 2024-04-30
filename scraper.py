from pyrogram import Client
from typing import AsyncGenerator
from pyrogram.types import Message

from config import API_ID, API_HASH

async def parser_content(donor_channel_id:int, my_channel_id:int) -> AsyncGenerator[Message, None]:
    async with Client('my_bot', api_id=API_ID, api_hash=API_HASH) as app:
        pass