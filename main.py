import asyncio
import json
from termcolor import colored
import disnake as discord
from disnake.ext import commands
import os

bot = commands.Bot(intents=discord.Intents.all(), command_prefix='?', owner_id=493370963807830016)
bot.remove_command('help')


@bot.event
async def on_ready():
    print(colored(f'Botid: {bot.user.id} - Name: {bot.user.name}#{bot.user.discriminator}', 'green'))
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f'?help | {len(bot.guilds)} servers'),
        status=discord.Status.idle)
    while True:
        await asyncio.sleep(10)
        with open("utils/json/spam-detection.json",
                  "r+") as file:
            file.truncate(0)


print(colored('COG PART', 'red'))
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        try:
            bot.load_extension(f'cogs.{filename[:-3]}')
            print(f'Loaded ' + colored(f'{filename} ', 'green') + f'Successful')
        except discord.Forbidden:
            print(colored(f'Error, something went wrong with {filename}!', 'red'))

print(colored('EVENT PART', 'red'))
for filename in os.listdir('./events'):
    if filename.endswith('.py'):
        try:
            bot.load_extension(f'events.{filename[:-3]}')
            print(f'Loaded ' + colored(f'{filename} ', 'green') + f'Successful')
        except discord.Forbidden:
            print(colored(f'Error, something went wrong with {filename}!', 'red'))

print(colored('LISTENER PART', 'red'))
for filename in os.listdir('./listener'):
    if filename.endswith('.py'):
        try:
            bot.load_extension(f'listener.{filename[:-3]}')
            print(f'Loaded ' + colored(f'{filename} ', 'green') + f'Successful')
        except discord.Forbidden:
            print(colored(f'Error, something went wrong with {filename}!', 'red'))

print(colored('Finished setting up files!', 'red'))

with open('etc/config.json', 'r') as config_file:
    config = json.load(config_file)

bot.run(config["token"]["token"])
