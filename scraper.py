from pyrogram import Client
from typing import AsyncGenerator
from pyrogram.types import Message

from config import API_ID, API_HASH


class Scraper:
    def __init__(self, client:Client, test_flag:bool=True) -> None:
        if test_flag:
            self.client = Client('test_bot', api_id=API_ID, api_hash=API_HASH)
        else:
            self.client =  client
    async def parser_content(donor_channel_id:int, my_channel_id:int) -> AsyncGenerator[Message, None]:
        async with Client('my_bot', api_id=API_ID, api_hash=API_HASH) as app:
            pass
        

if __name__ == '__main__':
    
    
    scraper = Scraper(client=)
