from pyrogram import Client
from typing import AsyncGenerator
from pyrogram.types import Message

import asyncio
import logging
import config


class Scraper:
    def __init__(self, client:Client=None, test_flag:bool=True) -> None:
        if test_flag:
            self.client = Client('test_aiassist_bot', api_id=config.API_ID_TEST, api_hash=config.API_HASH_TEST, phone_number=config.PHONE_NUMBER_TEST)
        else:
            self.client =  client
            
    async def parser_content(
            self, 
            donor_channel_id: int | str,
            limit_mess:int=50, 
            target_channel_id:str=config.MY_CHANNEL_ID
        ) -> AsyncGenerator[Message, None]:
        
        async with self.client as app:
            messages: AsyncGenerator[Message, None] = app.get_chat_history(chat_id=donor_channel_id, limit=limit_mess)
            
            async for message in messages:
                await message.copy(chat_id=target_channel_id)

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO, 
        format="%(asctime)s - %(levelname)s - %(message)s",
        )
    
    scraper = Scraper()
    
    asyncio.run(scraper.parser_content(donor_channel_id='-1001322370409', limit_mess=5))
