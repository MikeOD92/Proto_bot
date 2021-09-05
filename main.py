from replit import db
import discord
import os
import requests
import json
import random

client = discord.Client()
sad_words = ['bummer', 'sad', 'depressed', 'unhappy', 'gosh darn it']

starter_encouragements = [
  "cheer up kiddo", "hang in there", "you are a great person/bot", "wow way to go"
]

def get_quote():
  response = requests.get('https://zenquotes.io/api/random')

  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']

  return(quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    # encouraging_message.extends(db["encouragements"])
    encouragements = db.encouragements.append(encouraging_message)
    db['encouragements'] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragement(index):
  encouragements = db['encouragments']
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

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

  options = starter_encouragements

  if "encouragements" in db.keys():
    # options = options + db["encouragements"]
    options.extend(db["encouragements"])

  
  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(options))

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



client.run(os.environ['TOKEN'])
  


