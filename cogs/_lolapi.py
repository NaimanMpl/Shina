import discord
from discord.ext import commands
import requests
from riotwatcher import *

class LoLAPI(commands.Cog):

    key = ''

    def __init__(self, client):
        self.client = client

    watcher = RiotWatcher(key)
    region = 'euw1'
    username = 'ZelphiiX'

    @commands.command()
    async def lolstats(self, ctx, playername, region):
        key = ''
        watcher = RiotWatcher(key)

        player = watcher.summoner.by_name(region, playername)
        print(player , '\n')

        player_id = watcher.league.by_summoner(region, player['id'])
        #print(f'Statistiques Classés Flex 5x5:', player_id[1], '\n')

        #print('Statistiques Classés Solo/DuoQ :', player_id[1], '\n')

        

        await ctx.send(f"Stats Solo/DuoQ 5x5 : Rank : {player_id[0]['tier']} {player_id[0]['rank']} Wins : {player_id[0]['wins']} Défaites : {player_id[0]['losses']} Winrate : {int(player_id[0]['wins'] / (player_id[0]['wins']+player_id[0]['losses']) * 100)}%")
        #await ctx.send(f"Stats Flex 5x5 : Rank : {player_id[1]['tier']} {player_id[1]['rank']} {player_id[1]['leaguePoints']} LP Wins : {player_id[1]['wins']} Défaites : {player_id[1]['losses']} Winrate : {int(player_id[1]['wins'] / (player_id[1]['wins']+player_id[1]['losses'])* 100)}%")
        

        try:
            response = watcher.summoner.by_name(region, playername)
        except ApiError as err:
            if err.response.status_code == 429:
                print('We should retry in {} seconds.'.format(err.response.headers['Retry-After']))
                print('this retry-after is handled by default by the RiotWatcher library')
                print('future requests wait until the retry-after time passes')
            elif err.response.status_code == 404:
                await ctx.send('Je n\'arrive pas à trouver ce joueur !')
            else:
                raise


def setup(client):
    client.add_cog(LoLAPI(client))

