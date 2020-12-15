from telethon import TelegramClient, sync, events
from flask import Flask
from colorama import Fore, Back, Style
from telethon.tl.functions.messages import GetHistoryRequest, GetBotCallbackAnswerRequest
from telethon.errors import SessionPasswordNeededError
from telethon.errors import FloodWaitError
from time import sleep
import json,re,sys,os
import requests as r

try:
   import requests
   from bs4 import BeautifulSoup
except:
   print ("\\033[1;30m# \\033[1;31mHmmm Sepertinya Modul Requests Dan Bs4 Belum Terinstall\\n\\033[1;30m# \\033[1;31mTo install Please Type pip install requests and pip install bs4")
   sys.exit()

domain = 'https://ltcscript.kamakeparteam.repl.co'

c = requests.Session()
banner = "Hello user!"

if not os.path.exists("session"):
    os.makedirs("session")

print (banner)
if len(sys.argv)<2:
   print (Fore.RED +"Usage : python main.py +62")
   sys.exit(1)


def password():
  c = requests.Session()
  if not os.path.exists(".password"):
      os.makedirs(".password")

  print("http://t.me/kamakepar_man")
  me = str(input('Enter username: '))
  pw = r.get(domain+'/get_password.php?u='+me).text
  #print('Pas: '+pw)
  if not os.path.exists(".password/pass.txt"):
      f = open(".password/pass.txt", "w+")
      f.write("wkwkwkwkw")
      f.close()
  for i in range(99):
      f = open(".password/pass.txt", "r")
      if f.readlines()[0] == pw:
          sys.stdout.write("Using Exiting Password....!\n")
          break
      pwin = input("Enter Password: ")
      if pwin == pw:
          f = open(".password/pass.txt", "w+")
          f.write(pwin)
          f.close()
          break
      else:
          print("Password Entered...!")
          if i > 1:
              print(Fore.RED +"Check Password Per Link: https://ltcscript.kamakeparteam.repl.co/profile.php\n https://t.me/kamakepar_man")
              sys.exit()


def tunggu(x):
    sys.stdout.write("\\r")
    sys.stdout.write("                                                               ")
    for remaining in range(x, 0, -1):
       sys.stdout.write("\\r")
       print(Fore.RED + "{:2d} seconds remaining ".format(remaining))
       sys.stdout.flush()
       sleep(1)
ua={"User-Agent": "Mozilla/5.0 (Linux; Android 5.1; A1603 Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36"}


api_id = 1210596
api_hash = "6ef3dd7dfe4e4f82f797e899cbdd0056"
phone_number = sys.argv[1]
client = TelegramClient("session/"+phone_number, api_id, api_hash)
client.connect()
if not client.is_user_authorized():
  try:
    client.send_code_request(phone_number)
    me = client.sign_in(phone_number, input("Enter your code"))
  except SessionPasswordNeededError:
   passw = input("\\033[1;0mYour 2fa Password : ")
   me = client.start(phone_number,passw)
myself = client.get_me()
os.system("clear")
print (banner)
print (Fore.GREEN +"Welcome To TeleBot ",myself.first_name,"Fucking LTC Click Bot")



password()
print (Fore.BLUE +"Starting......!")
try:
 channel_entity=client.get_entity("@Litecoin_click_bot")
 channel_username="@Litecoin_click_bot"
 for i in range(5000000):
  sys.stdout.write("                                                              ")
  sys.stdout.write("")
  print(Fore.GREEN + 'Loading urls...')
  sys.stdout.flush()
  client.send_message(entity=channel_entity,message="\xf0\x9f\x96\xa5 Visit sites")
  sleep(3)
  posts = client(GetHistoryRequest(peer=channel_entity,limit=1,offset_date=None,offset_id=0,max_id=0,min_id=0,add_offset=0,hash=0))
  if posts.messages[0].message.find("Sorry, there are no new ads available") != -1:
     print ("No new ads availible :-(")
     client.send_message(entity=channel_entity,message="\xf0\x9f\x92\xb0 Balance")
     sleep(5)
     posts = client(GetHistoryRequest(peer=channel_entity,limit=1,offset_date=None,offset_id=0,max_id=0,min_id=0,add_offset=0,hash=0))
     message = posts.messages[0].message
     print (message)
     sys.exit()
  else:
    try:
     url = posts.messages[0].reply_markup.rows[0].buttons[0].url
     sys.stdout.write("Visit "+url+"\n")
     sys.stdout.flush()
     id = posts.messages[0].id
     r = c.get(url, headers=ua, timeout=15, allow_redirects=True)
     soup = BeautifulSoup(r.content,"html.parser")
     if soup.find("div",class_="g-recaptcha") is None and soup.find("div", id="headbar") is None:
        sleep(2)
        posts = client(GetHistoryRequest(peer=channel_entity,limit=1,offset_date=None,offset_id=0,max_id=0,min_id=0,add_offset=0,hash=0))
        message = posts.messages[0].message
        if posts.messages[0].message.find("You must stay") != -1 or posts.messages[0].message.find("Please stay on") != -1:
           sec = re.findall('([\\d.]*\\d+)', message)
           tunggu(int(sec[0]))
           sleep(1)
           posts = client(GetHistoryRequest(peer=channel_entity,limit=2,offset_date=None,offset_id=0,max_id=0,min_id=0,add_offset=0,hash=0))
           messageres = posts.messages[1].message
           sleep(2)
           print(Fore.RED +"[*] Message: "+messageres)
        else:
           pass



     elif soup.find('div', id="headbar") is not None:
        for dat in soup.find_all('div',class_="container-fluid"):
            code = dat.get('data-code')
            timer = dat.get('data-timer')
            tokena = dat.get('data-token')
            tunggu(int(timer))
            r = c.post("https://dogeclick.com/reward",data={"code":code,"token":tokena}, headers=ua, timeout=15, allow_redirects=True)
            js = json.loads(r.text)
            print(Fore.YELLOW + "You earned "+js['reward']+" LTC for visiting a site!")
     else:
        sys.stdout.write("")
        sys.stdout.write("                                                                ")
        sys.stdout.write("")
        print(Fore.BLUE + "Captcha Detected")
        sys.stdout.flush()
        sleep(2)
        client(GetBotCallbackAnswerRequest(channel_username,id,data=posts.messages[0].reply_markup.rows[1].buttons[1].data        ))
        print(Fore.GREEN +"Skiping Captcha...!")
        sleep(2)
    except:
        sleep(3)
        posts = client(GetHistoryRequest(peer=channel_entity,limit=1,offset_date=None,offset_id=0,max_id=0,min_id=0,add_offset=0,hash=0))
        message = posts.messages[0].message
        if posts.messages[0].message.find("You must stay") != -1 or posts.messages[0].message.find("Please stay on") != -1:
           sec = re.findall('([\\d.]*\\d+)', message)
           tunggu(int(sec[0]))
           sleep(1)
           posts = client(GetHistoryRequest(peer=channel_entity,limit=2,offset_date=None,offset_id=0,max_id=0,min_id=0,add_offset=0,hash=0))
           messageres = posts.messages[1].message
           sleep(2)
           print(Fore.RED +messageres)
        else:
           pass

finally:
   client.disconnect()
