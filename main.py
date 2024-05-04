from pyrogram.handlers import MessageHandler
from pyrogram import Client, idle
from pyrogram.types import Message

import asyncio
import logging
import config


async def get_channel_id(client: Client, message: Message) -> int:
    print(message)
    

async def main():
	async with Client("test_aiassist_bot", api_id=config.API_ID_TEST, api_hash=config.API_HASH_TEST) as app:
		app.add_handler(MessageHandler(get_channel_id))
		await idle()


if __name__ == '__main__':
	logging.basicConfig(
		level=logging.INFO, 
		format="%(asctime)s - %(levelname)s - %(message)s",
		)
	asyncio.run(main())