from pyrogram import Client, idle
from typing import AsyncGenerator
from pyrogram.types import Message, List
from pyrogram.raw.functions.channels import GetFullChannel

import asyncio
import logging
import config

from utils import Utils

class Scraper:
    # def __init__(self, client:Client=None, test_flag:bool=True) -> None:
    #     if test_flag:
    #         self.client = Client('test_aiassist_bot', api_id=config.API_ID_TEST, api_hash=config.API_HASH_TEST)#, phone_number=config.PHONE_NUMBER_TEST
    #     else:
    #         self.client =  client
    @Utils.decorator_timer
    async def parser_content_open_example(
            self, 
            donor_channel_id: int | str,
            limit_mess:int=50, 
            target_channel_id:str=config.MY_CHANNEL_ID
        ) -> AsyncGenerator[Message, None]:
        
        async with Client("test_aiassist_bot", api_id=config.API_ID_TEST, api_hash=config.API_HASH_TEST) as app:
            messages: AsyncGenerator[Message, None] = app.get_chat_history(chat_id=donor_channel_id, limit=limit_mess)
            
            reversed_messages = await self._reversed_messages(messages)
            cnt = 0
            to_send = {'videos':[], 'animations':[], 'texts':[]}
            for message in reversed_messages:
                if cnt == 3:
                    break
                
                
                if message.animation:
                    print('Нашли анимацию')
                    animation = await message.download(in_memory=True)
                    to_send['animations'].append(animation)
                elif message.video:
                    print('Нашли видео')
                    video = await message.download(in_memory=True)
                    to_send['videos'].append(video)
                    # if message.caption:
                    #     await app.send_video(chat_id=target_channel_id, video=video, caption=message.caption.html)
                    # else:
                    #     await app.send_video(chat_id=target_channel_id, video=video)
                elif message.text:
                    to_send['texts'].append(message.text)
                    cnt += 1
                    if len(to_send['videos'])>0:
                        app.send_video(chat_id=target_channel_id, video=to_send['videos'][0], caption=to_send['texts'][0])
                    elif len(to_send['animations'])>0:
                        app.send_animation(chat_id=target_channel_id, video=to_send['animations'][0], caption=to_send['texts'][0])
                    print('Нашли text', to_send.__dict__)
                    # elif len(to_send['texts'])>0:
                    # app.send_message
                    to_send = {'videos':[], 'animations':[], 'texts':[]}
                # # await message.copy(chat_id=target_channel_id)

    @Utils.decorator_timer
    async def parser_content_closed_example(
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

    @Utils.decorator_timer
    async def parser_members(
            self, 
            donor_channel_id: int | str,
            limit_mess:int=50, 
            target_channel_id:str=config.MY_CHANNEL_ID
        ) -> AsyncGenerator[Message, None]:
        
        async with Client("test_aiassist_bot", api_id=config.API_ID_TEST, api_hash=config.API_HASH_TEST) as app:
            members: AsyncGenerator[Message, None] = app.get_chat_members(chat_id=donor_channel_id, limit=limit_mess)
        
            with open('members.txt', 'w') as f:
                async for member in members:
                    f.write(f'{member.user.first_name} {member.user.last_name} {member.user.username} {member.user.id}\n')


    async def _reversed_messages(self, messages: AsyncGenerator[Message, None]) -> AsyncGenerator[Message, None]:
        reverse_message = [message async for message in messages]
        return reverse_message[::-1]
        
if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO, 
        format="%(asctime)s - %(levelname)s - %(message)s",
        )
    scraper = Scraper()
    # asyncio.run(scraper.parser_content_closed(donor_channel_id=-1001983581219, limit_mess=3))# vgtimes id = -1001338358512, pornhub_prem id = -1001322370409
    asyncio.run(scraper.parser_content_open_example(donor_channel_id=-1001322370409, limit_mess=50))# vgtimes id = -1001338358512