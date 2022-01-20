import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantAdmin
from telethon.tl.types import ChannelParticipantCreator
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)
spam_chats = []

@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply(
    "__**I'm 《𝐁𝐇𝐀𝐓𝐀𝐊𝐓𝐈 𝐀𝐓𝐌𝐀 𝐌𝐞𝐧𝐭𝐢𝐨𝐧 𝐑𝐨𝐛𝐨𝐭》**, 𝐇𝐘𝐘, 𝐈 𝐀𝐌 𝐌𝐄𝐍𝐓𝐈𝐎𝐍 𝐀𝐋𝐌𝐎𝐒𝐓 𝐓𝐀𝐆 𝐀𝐋𝐋 𝐌𝐄𝐌𝐁𝐄𝐑 𝐆𝐑𝐎𝐔𝐏 𝐀𝐍𝐒 𝐂𝐇𝐀𝐍𝐍𝐄𝐋👻\n𝐂𝐋𝐈𝐂𝐊**/help** 𝐅𝐎𝐑 𝐌𝐎𝐑𝐄 𝐈𝐍𝐅𝐎𝐑𝐌𝐀𝐓𝐈𝐎𝐍__\n\n 𝐒𝐔𝐏𝐏𝐎𝐑𝐓 [🔥𝐁𝐇𝐀𝐓𝐀𝐊𝐓𝐈𝐀𝐓𝐌𝐀🚩](https://t.me/SUBHI_WORLD) 𝐈𝐍 𝐓𝐄𝐋𝐄𝐆𝐑𝐀𝐌",
    link_preview=False,
    buttons=(
      [
        Button.url('📣 Channel', 'https://t.me/A_BUT'),
          Button.url('👑 OWNER', 'https://t.me/ZINDA_H_TU_MERE_LIYE_HEART_HACK'),
          Button.url('👑 C-OWNER', 'https://t.me/Itz_me_baby'),
        Button.url('⚜️ GROUP', 'https://t.me/SUBHI_WORLD')
      ]
    )
  )

@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "**Help Menu of MentionAllBot**\n\nCommand: /mentionall\n__You can use this command with text what you want to mention others.__\n`Example: /mentionall Good Morning!`\n__You can you this command as a reply to any message. Bot will tag users to that replied messsage__.\n\Support [𝐁𝐇𝐀𝐓𝐀𝐊𝐓𝐈 𝐀𝐓𝐌𝐀](https://t.me/A_BUT) on Telegram"
  await event.reply(
    helptext,
    link_preview=False,
    buttons=(
      [
        Button.url('📣 Channel', 'https://t.me/A_BUT'), 
        Button.url('👑 OWNER', 'https://t.me/ZINDA_H_TU_MERE_LIYE_HEART_HACK'),
        Button.url('📦 Source', 'https://t.me/SUBHI_WORLD')
      ]
    )
  )
  
@client.on(events.NewMessage(pattern="^/mentionall ?(.*)"))
async def mentionall(event):
  chat_id = event.chat_id
  if event.is_private:
    return await event.respond("__This command can be use in groups and channels!__")
  
  is_admin = False
  try:
    partici_ = await client(GetParticipantRequest(
      event.chat_id,
      event.sender_id
    ))
  except UserNotParticipantError:
    is_admin = False
  else:
    if (
      isinstance(
        partici_.participant,
        (
          ChannelParticipantAdmin,
          ChannelParticipantCreator
        )
      )
    ):
      is_admin = True
  if not is_admin:
    return await event.respond("__Only admins can mention all!__")
  
  if event.pattern_match.group(1) and event.is_reply:
    return await event.respond("__Give me one argument!__")
  elif event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.is_reply:
    mode = "text_on_reply"
    msg = await event.get_reply_message()
    if msg == None:
        return await event.respond("__I can't mention members for older messages! (messages which are sent before I'm added to group)__")
  else:
    return await event.respond("__Reply to a message or give me some text to mention others!__")
  
  spam_chats.append(chat_id)
  usrnum = 0
  usrtxt = ''
  async for usr in client.iter_participants(chat_id):
    if not chat_id in spam_chats:
      break
    usrnum += 1
    usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
    if usrnum == 5:
      if mode == "text_on_cmd":
        txt = f"{usrtxt}\n\n{msg}"
        await client.send_message(chat_id, txt)
      elif mode == "text_on_reply":
        await msg.reply(usrtxt)
      await asyncio.sleep(2)
      usrnum = 0
      usrtxt = ''
  try:
    spam_chats.remove(chat_id)
  except:
    pass

@client.on(events.NewMessage(pattern="^/cancel$"))
async def cancel_spam(event):
  if not event.chat_id in spam_chats:
    return await event.respond('__There is no proccess on going...__')
  else:
    try:
      spam_chats.remove(event.chat_id)
    except:
      pass
    return await event.respond('__Stopped.__')

print(">> BHATAKTI ATMA MENTION BOT STARTED <<")
client.run_until_disconnected()
