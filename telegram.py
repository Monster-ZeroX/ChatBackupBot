#code by Jaindu Charindith
#t.me/charindith
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from time import sleep
from requests import post
import pytz,os

TG_API='https://api.telegram.org/bot'
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
TOKEN=os.getenv("BOT_TOKEN")
BOT_url=TG_API + TOKEN
log_users=[os.getenv("LOG_CHANNEL")]
ownerunam=os.getenv("OWNER_UNAME")
session=os.getenv("SESSION")
client = TelegramClient(StringSession(session), api_id, api_hash)
def botSend(fileName, tes ,pat):
    files = {pat: (fileName, open(fileName,'rb'))}
    for log_user in log_users:
        r = post(BOT_url+tes+'&chat_id='+log_user, files=files)        
def utc_to_time(naive, timezone="Asia/Kolkata"):
    return naive.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(timezone))
def dirup(event,sender,pat,tgapi):
    tes =tgapi+'?caption=@'+ str(sender.username)+"\n"+str(event.text)+"\n"+str(utc_to_time(event.date))
    arr = os.listdir(pat)
    for files in arr:
        path=pat+"/"+str(files)
        botSend(path,tes,pat)
        sleep(1)
        os.remove(path)

@client.on(events.Album)
async def handler(event):
    if event.is_private:
        await event.forward_to(log_users[0])

@client.on(events.NewMessage)
async def my_event_handler(event):
    sender = await event.get_sender()
    if event.is_private:        
        if event.photo or event.video or event.document or event.audio:
            if event.photo:
                pat='photo'
                tgapi='/sendPhoto'
            elif event.video:
                pat='video'
                tgapi='/sendvideo'    
            else:
                pat='document'
                tgapi='/sendDocument'
            await event.download_media(file=pat)
            sleep(2)
            await dirup(event,sender,pat,tgapi)
        else:
            tes ="@"+ str(sender.username)+"\n"+str(event.text)+"\n"+str(utc_to_time(event.date))
            eentity = await client.get_entity(event.original_update.user_id)
            print(eentity.username)
            if sender.username==ownerunam:
                tes ="@"+ownerunam+" to @"+ str(eentity.username)+"\n"+str(event.text)+"\n"+str(utc_to_time(event.date))
            for log_user in log_users:
                g=post(BOT_url+'/sendmessage' , json={"chat_id":log_user,"text":tes})
                print(g.text)
print('bot started\nBY Dasun(t.me/dasun_pamod)')
client.start()
client.run_until_disconnected()
