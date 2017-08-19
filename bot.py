import discord
import json
import asyncio
import config
import requests
import urllib.parse
import random

client = discord.Client()

YOUTUBE_SEARCH_URL_START = 'https://www.googleapis.com/youtube/v3/search?part=id&type=video&q='
YOUTUBE_SEARCH_URL_END = '&key='
YOUTUBE_WATCH_URL = 'https://www.youtube.com/watch?v='
WHO_LET_THE_DOGS_OUT = 'Qkuu0Lwb5EM'


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-------')

@client.event
async def on_message(message):
    content = message.content.lower()

    # respond with user
    if message.content.startswith('!test'):
        user = message.author
        await client.send_message(message.channel, user)

    # respond with random 'magic 8 ball' answer to question
    elif message.content.startswith('!ask'):
        answer = random.choice(['Yes', 'No', 'Who cares?', 'Fuck off'])
        await client.send_message(message.channel, answer)

    
    # responds with coin flip
    elif message.content.startswith('!flip'):
        answer = random.choice(['Heads', 'Tails'])
        await client.send_message(message.channel, answer)

    # respond with who let the dogs out video
    elif message.content.startswith('!who'):
        await client.send_message(message.channel, YOUTUBE_WATCH_URL + WHO_LET_THE_DOGS_OUT)

    # respond with first youtube search item based on search criteria
    elif message.content.startswith('!getyoutube'):
        query = content.split("!getyoutube ", 1)[1]

        response = requests.get(YOUTUBE_SEARCH_URL_START + urllib.parse.quote(query, safe='~()*!.\'') + YOUTUBE_SEARCH_URL_END + config.YoutubeKey())
        data = response.json()
        videoId = data['items'][0]['id']['videoId']

        await client.send_message(message.channel, YOUTUBE_WATCH_URL + videoId)


client.run(config.BotToken())

