from telethon import TelegramClient, events, utils
from telethon.tl.types import (
    InputMessagesFilterRoundVideo
)
from config import API_ID, API_HASH, SESSION, CHATS, DESTINATION
import time

client = TelegramClient(SESSION, API_ID, API_HASH)
mid1 = 0

async def main():
    try:
        global mid1
        start = 0
        finish = 1000
        for i in range(start, finish):
            try:
                async for mess in client.iter_messages(CHATS, min_id=i-1, max_id=i+1, filter=InputMessagesFilterRoundVideo):
                print('Текущее сообщение '+i)
                if mess.is_reply:
                    mid = mess.reply_to.reply_to_msg_id
                    repl = await client.get_messages(CHATS, ids=mid)
                    user = await client.get_entity(repl.from_id.user_id)
                    if mid1 == mid:
                        await client.send_message(DESTINATION, mess)
                        mid = 0
                        mess = None
                    else:
                        client.parse_mode = 'html'
                        link = CHATS +"/"+str(mid)
                        linkfull = f'<a href={link}>link</a>'
                        await client.send_message(DESTINATION, '#'+user.username+" "+repl.message+"\n"+linkfull, link_preview = False, file = repl.media)
                        await client.send_message(DESTINATION, mess)
                        mid1 = mid
                        mess = None
                            
                else:
                    await client.send_message(DESTINATION, mess)
                    mess = None
                        
            except Exception:
                continue

    except Exception as ex:
        print(f'Exception: {ex}')

print("Program is running...")
with client:
    client.loop.run_until_complete(main())
