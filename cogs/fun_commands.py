import discord
from discord.ext import commands
import imageslist
import random
from random import randint
import smug_images_list

class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def hug(self, ctx, member : discord.User = None):

        # Embed

        images_list = imageslist.get_imagees_list()

        hug_count = 0
        message_author = ctx.message.author.display_name

        if member:
            embed = discord.Embed(
                title = None,
                description = f'{message_author} fait un calin à {member}',
                colour = discord.Colour.purple()
                )
            hug_count = hug_count + 1
            embed.set_footer(text=f'C\'est le {hug_count}eme calin que Shina donne !')
            embed.set_image(url= random.choice(images_list))

            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title = None,
                description = f'{message_author} se fait un calin',
                colour = discord.Colour.blue()
                )
            hug_count = hug_count + 1
            embed.set_footer(text=f'C\'est le {hug_count}eme calin que Shina donne !')
            embed.set_image(url= random.choice(images_list))

            await ctx.send(embed=embed)

    @commands.command()
    async def smug(self, ctx, member : discord.Member = None):

        images_list = smug_images_list.get_images_list()
        message_author = ctx.message.author.display_name
        hug_count = 0

        if member:
            embed = discord.Embed(
                title = None,
                description = f'{message_author} fait un smug à {member}',
                colour = member.color
                )
            hug_count = hug_count + 1
            embed.set_footer(text=f'C\'est le {hug_count} smug que Shina donne !')
            embed.set_image(url=random.choice(images_list))

            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title = None,
                description = f'{message_author} smug',
                colour = member.color
                )
            hug_count = hug_count + 1
            embed.set_footer(text=f'C\'est le {hug_count} smug que Shina donne !')
            embed.set_image(url= random.choice(images_list))

            await ctx.send(embed=embed)
        

    @commands.command()
    async def roulette(self, ctx, *, args):

        server_members_list = ctx.message.guild.members
        await ctx.send(f'Le gagnant du **{args}** est : {server_members_list[randint(0, len(server_members_list)-1)].name}')


def setup(client):
    client.add_cog(Fun(client))


