from replit import db
import discord
import os
import requests
import json
import random

client = discord.Client()

sad_words = ['bummer', 'sad', 'depressed', 'unhappy']

starter_encouragements = [
  "cheer up kiddo", "hang in there", "you are a great person/bot", "wow way to go"
]

char_sheet = [
  {
  "attr": "strength",
  "value": 0
  },
  {
    "attr": "agility",
    "value": 0
  },
  {
    "attr": "wisdom",
    "value": 0
  },

]

def get_quote():
  response = requests.get('https://zenquotes.io/api/random')

  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']

  return(quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    db['encouragements'].append(encouraging_message)
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragement(index):
  encouragements = db['encouragements']
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

if "encouragements" in db.keys():
    options = starter_encouragements
    options.extend(db["encouragements"])
#moving this up here lets us avoid added the entire db object to it's self when we add a new one but now the new string does not append correctly 

@client.event
async def on_ready():
  print('we have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content
  
  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(db["encouragements"]))
    #changed this from options to encouragements seems to work had wrong print in next line so double checking now

    # await message.channel.send(db['encouragements'])

  if msg.startswith('$new'):
    encouraging_message = msg.split('$new ',1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send('new encouragement message added' + "''" + encouraging_message + "''")

  if msg.startswith('$del'):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split('$del',1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]
      await message.channel.send(encouragements)
# dice roll functionality for RPG-roll bot (next project)
  if msg.startswith('/roll'):
    roll = msg.split('/roll', 1)[1]

    if(roll.split('d')[0] == " " or roll.split('d')[0] == "" ):
      num = 1
    else:
      num = int(roll.split('d')[0])

    sides = int(roll.split('d')[1])

    await message.channel.send(str(message.author) + " rolled " +str(roll))
    
    total = 0

    while num > 0:
      rolled_num = random.randint(1,sides)
      total = rolled_num + total
      await message.channel.send(rolled_num)
      num -= 1
    await message.channel.send('total val is ' + str(total))  
    return total

  if msg.startswith('$hey'):
    #added emoji with :slight_smile: or :flag_us: etc...
    await message.channel.send("Hi :slight_smile:")

    await message.channel.send(db["encouragements"])

  if msg.startswith('/createchar'):
    db[message.author] = char_sheet

    for item in char_sheet:
      await message.channel.send(f'roll for your {item["attr"]}')
      # await client.wait_for("message", check=lambda: message.author == 'ctx'.author )
      

    

    
    






client.run(os.environ['TOKEN'])
  


