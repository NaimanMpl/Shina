import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import time
import random
from random import randint

members_list = []

class Roulette(commands.Cog):

    def __init__(self, client):
        self.client = client

    @has_permissions(administrator=True)
    @commands.command()
    async def rr(self, ctx, add, member : discord.Member = None):

        self.add = "add"
        message_author = ctx.message.author.display_name

        if not member:
            await ctx.send("Tu dois renseigner un joueur !")
        elif not member.display_name in members_list:

            members_list.append(member.display_name)
            print(members_list)
            await ctx.send(f'{member.display_name} a bien été ajouté à la liste de participants !')
            await ctx.send(f'Liste de joueurs : {members_list}, Taille de la liste : {len(members_list)}')

    @has_permissions(administrator=True)
    @commands.command()
    async def rrstart(self, ctx):

        if len(members_list) <= 1:
            await ctx.send("Il n'y a pas assez de participants !")
            return

        timer = 5

        while timer != 0:

            await ctx.send(f'La roulette russe commence dans : {timer}')

            time.sleep(1)

            timer -= 1

        if timer == 0:
            while len(members_list) != 1:
                await ctx.send("Here we go! :ye:")
                await ctx.send("Qui aura droit au chatiment divin ? :pensive:")
                time.sleep(20)
                member_dead = members_list[randint(0, len(members_list)-1)]
                await ctx.send(f'Aïe | ||**{member_dead}**|| est mort.')               
                members_list.remove(member_dead)
                await ctx.send(f'**Joueurs restants | {members_list}')
                time.sleep(15)

        if len(members_list) == 1:
            await ctx.send(f'Roulette Russe | **{members_list[0]}** a gagné la partie ! @here')



def setup(client):
    client.add_cog(Roulette(client))