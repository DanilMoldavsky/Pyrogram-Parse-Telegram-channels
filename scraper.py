from pyrogram import Client, idle
from typing import AsyncGenerator
from pyrogram.types import Message, List

import asyncio
import logging
import config


class Scraper:
    # def __init__(self, client:Client=None, test_flag:bool=True) -> None:
    #     if test_flag:
    #         self.client = Client('test_aiassist_bot', api_id=config.API_ID_TEST, api_hash=config.API_HASH_TEST)#, phone_number=config.PHONE_NUMBER_TEST
    #     else:
    #         self.client =  client
            
    async def parser_content_open(
            self, 
            donor_channel_id: int | str,
            limit_mess:int=50, 
            target_channel_id:str=config.MY_CHANNEL_ID
        ) -> AsyncGenerator[Message, None]:
        
        async with Client("test_aiassist_bot", api_id=config.API_ID_TEST, api_hash=config.API_HASH_TEST) as app:
            messages: AsyncGenerator[Message, None] = app.get_chat_history(chat_id=donor_channel_id, limit=limit_mess)
            
            reversed_messages = await self._reversed_messages(messages)
            
            for message in reversed_messages:
                await message.copy(chat_id=target_channel_id)

    async def parser_content_closed(
            self, 
            donor_channel_id: int | str,
            limit_mess:int=50, 
            target_channel_id:str=config.MY_CHANNEL_ID
        ) -> AsyncGenerator[Message, None]:
        
        async with Client("test_aiassist_bot", api_id=config.API_ID_TEST, api_hash=config.API_HASH_TEST) as app:
            messages: AsyncGenerator[Message, None] = app.get_chat_history(chat_id=donor_channel_id, limit=limit_mess)
            
            reversed_messages: List[Message] = await self._reversed_messages(messages)
            
            for message in reversed_messages:
                if message.video:
                    video = await message.download(in_memory=True)
                    if message.caption:
                        await app.send_video(chat_id=target_channel_id, video=video, caption=message.caption.html)
                    else:
                        await app.send_video(chat_id=target_channel_id, video=video)
                elif message.photo:
                    photo = await message.download(in_memory=True)
                    if message.caption:
                        await app.send_photo(chat_id=target_channel_id, photo=photo, caption=message.caption.html)
                    else:
                        await app.send_photo(chat_id=target_channel_id, photo=photo)
                else:
                    await app.send_message(chat_id=target_channel_id, text=message.text)



    async def _reversed_messages(self, messages: AsyncGenerator[Message, None]) -> AsyncGenerator[Message, None]:
        reverse_message = [message async for message in messages]
        return reverse_message[::-1]
        
if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO, 
        format="%(asctime)s - %(levelname)s - %(message)s",
        )
    scraper = Scraper()
    asyncio.run(scraper.parser_content_closed(donor_channel_id=-1001983581219, limit_mess=3))# vgtimes id = -1001338358512
