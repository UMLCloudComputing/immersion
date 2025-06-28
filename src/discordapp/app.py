import discord
import os

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('$ping'):
            await message.channel.send('Pong!')

client.run(os.getenv('DISCORD_TOKEN'))