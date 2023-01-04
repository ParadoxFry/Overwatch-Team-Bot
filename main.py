import discord

clinet = discord.Client()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client)))

@client.event
async def on_message(message):
  #this is where we implement how the bot responds to messages
  if message.author == client.user:
    return

  if message.content.startswith('!help'):
    #output some stuff
    return
    
  if message.content.startswith('!whoComp'):
    #list the users in the registration queue
    return

  if message.content.startswith('!comp'):
    #register to play
    return

  if message.content.startswith('!clearComp'):
    #reset the registration list
    return
  
  if message.content.startswith('!noComp'):
    #remove a user from from the list of registered comp users
    return

  if message.content.startswith('!makeTeams'):
    #Do the thing!
    return

