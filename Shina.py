import discord
from discord.ext import commands
from sqlconnection import Database
import os
import mysql.connector
import json

config_file = open('./config.json', 'r')
config_data = config_file.read()

parsed_config = json.loads(config_data)
print(parsed_config)

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='shina ', intents=intents)
token = parsed_config['Bot_Token']
mydb = Database(
    parsed_config['Host'],
    parsed_config['Database'],
    parsed_config['User'],
    parsed_config['Password']
)

PREFIX = '**Shina** »'
ANNOUNCE_CHANNEL_ID = parsed_config['Announce_Channel_ID']
EXP_GIVEN_PER_MINUTES = parsed_config['EXP_GIVEN_PER_MINUTES']
db = mysql.connector.connect(
    host=mydb.host,
    user=mydb.user,
    password=mydb.pwd,
    database=mydb.database,
)

users = {}
admins = {}
calls = {}
running_tasks = {}

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('I refuse.'))
    print('Shina est désormais connecté !')

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

def get_announce_channel():
    return client.get_channel(ANNOUNCE_CHANNEL_ID)

for filename in os.listdir("./cogs"):
    if filename.endswith('.py') and not filename.startswith("_"):
        client.load_extension(f'cogs.{filename[:-3]}')
        
client.run(token)
