#Imports
import discord
import os
import requests
import json
import urllib
import random
from keep_alive import keep_alive
from replit import db
#Variables
client = discord.Client()

help_data = [
     ">>> **Help Commands** \n\nThese are the available commands:\n\n1. `!bot help` - Dailogue of all commands\n2. `!bot info` - Gives info of bot\n3. `!bot quote` - presents quote\n4. `!bot meme` - presents meme\n5. `!bot joke` - presents a joke\n6. `!bot search github` - searches the user on github\n\n_This bot is Open Source_"
]

#Setting up function for Quotes
def get_quote():
    response = requests.get(
        "https://zenquotes.io/api/random")  #API uses Random Quotes
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " - " + json_data[0]['a']
    return (quote)

#Function to return random meme images URL
def random_meme():
  url =  "https://some-random-api.ml/meme"
  response = urllib.request.urlopen(url)
  data = json.loads(response.read())
  path = data["image"]
  return path

#Function to return random jokes 
def random_joke():
  url = "https://some-random-api.ml/joke"
  response = urllib.request.urlopen(url)
  data = json.loads(response.read())
  joke = data["joke"]
  return joke

#Function which return a github url
def github_search_user(user_name_to_search):
  response = urllib.request.urlopen("https://api.github.com/users/" + user_name_to_search )
  data = json.loads(response.read())
  github_url = data["html_url"]
  github_repos = data["repos_url"]
  github_resource = [github_url,github_repos]
  return github_resource

#Setting up function for adding projects
def newProject(projectTitle, projectType):
  new_project = projectTitle, projectType
  if "projects" in db.keys():
    projects = db["projects"]
    projects.append(new_project)
    db["projects"] = projects
  else:
    db["projects"] = projects

def removeProject(index):
  projects = db["projects"]
  if len(projects) > index:
    del projects[index]
    db["projects"] = projects

#Creating Login message
@client.event
async def on_ready():
    print('Bot is now live as {0.user}'.format(client))

@client.event
async def on_message(message):
    #Variables Ease
    msg = message.content

    #Condition for self texting
    if message.author == client.user:
        return

#Condition help
    if msg.startswith('!bot help'):
        await message.channel.send(''.join(help_data))

#Condition info
    if msg.startswith('!bot info'):
        await message.channel.send('>>> Bot v1.0.0')

#Condition requesting Quotes
    if msg.startswith('!bot quote'):
        quote = get_quote()
        await message.channel.send('>>> ' + '_' + quote + '_')

#Condition to return random meme
    if msg.startswith('!bot meme'):
      meme = random_meme()
      await message.channel.send(meme)

#Condition to return random jokes
    if msg.startswith('!bot joke'):
      joke = random_joke()
      await message.channel.send(">>> " + joke)

#Condition for searching a user in github
    if msg.startswith("!bot search github"):
      user_to_be_searched = msg.split(" ",3)[3]
      github_result = github_search_user(user_to_be_searched)
      await message.channel.send(">>> " + github_result[0])

#Condition to view projects
    if msg.startswith("!bot list projects"):
      projects = db["projects"].value
      for projectTitle, projectType in projects:
        await message.channel.send("{} | {} ".format(projectTitle, projectType))

#Condition to Add Projects
    if msg.startswith("!bot new project"):
      project_msg_array = msg.split("|")
      projectTitle = project_msg_array[1]
      projectType = project_msg_array[2]
      newProject(projectTitle, projectType)
      await message.channel.send(">>> Project Added")

#Condition to Delete Project
    if msg.startswith("!bot project completed"):
      index = int(msg.split("!bot project completed",1)[1])
      removeProject(index)
      await message.channel.send(">>> Project Completed")

#Keep Alive
keep_alive()

client.run(os.getenv('botTOKEN'))