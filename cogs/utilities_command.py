import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio
import random
import sys
sys.path.append('./')
from Shina import PREFIX

class Utilities(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def clear(self, ctx, default_amount=5):
        await ctx.channel.purge(limit=default_amount+1)
        message = await ctx.send(f'**Shina** a supprimé **{default_amount}** messages !')
        await asyncio.sleep(4)
        await message.delete()

    @commands.command()
    async def say(self, ctx, *, args):
        await ctx.send(f'{args}')

    @commands.command()
    async def choose(self, ctx, *, args):

        msg_list = ['Hmm.. Je pense que le meilleur choix est ',
                    'Laisse moi réfléchir.. La meilleure solution est ',
                    'Pourquoi tu me demandes ça ? C\'est obvious que le meilleur choix est ' 
        ]

        args_list = args.split('|')

        choice = random.choice(args_list)

        await ctx.send(f'{random.choice(msg_list)}{choice}')

    @has_permissions(administrator=True)
    @commands.command()
    async def goulag(self, ctx, member : discord.Member, *, reason):
        user = ctx.message.author
        role = discord.utils.get(user.guild.roles, name="Goulag")
        await member.add_roles(role)
        await ctx.send(f'Shina a bien donné ce que méritait **{member}** pour avoir énervé **{user}** ! Raison : {reason}')


def setup(client):
    client.add_cog(Utilities(client))



