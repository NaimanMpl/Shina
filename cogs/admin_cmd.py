import discord
from discord import guild
from discord.ext import commands
from discord.ext.commands import has_permissions
from Shina import users, admins, PREFIX
import user as userm
from user import User, admin

class AdminCmd(commands.Cog):

    def __init__(self, client : discord.Client):
        self.client = client

    @commands.command()
    async def addxp(self, ctx, member : discord.Member=None, amount : int=None):
        guild = member.guild
        if not member:
            await ctx.send('{PREFIX} Veuillez renseigner un membre !')
            return
        elif not amount:
            await ctx.send('{PREFIX} Veuillez renseigner un montant !')
            return
        elif amount <= 0:
            await ctx.send(f'{PREFIX} Le montant doit être supérieur ou égale à 1 !')
            return
        if (member.id, member.guild.id) in users:
            user = userm.get_user_by_id(member, member.guild)
        else:
            if not userm.exist(member, member.guild):
                await ctx.send('{PREFIX} Cet utilisateur n\'existe pas dans ce serveur !')
                return
            user = userm.load_user(member, member.guild)
        author = userm.load_user(ctx.message.author, ctx.message.author.guild)
        if not userm.exist(author, member.guild):
            await ctx.send(f"{PREFIX} Tu n\'es pas enregistré dans la base de données !")
            return
        if author.superuser or (author.get_id(), author.guild.id) in admins:
            userm.set_xp(user, member.guild, user.get_xp() + amount)
            await ctx.send(f"{PREFIX} a ajouté **{amount}** d\'expériences à {user.get_username() + user.get_discriminator()}, il passe niveau {user.get_level()}")
        else:
            await ctx.send(f"{PREFIX} Tu n'as pas la permission !")

    @commands.command()
    async def removexp(self, ctx, member : discord.Member=None, amount : int=None):
        guild = member.guild
        if not member:
            await ctx.send('{PREFIX} Veuillez renseigner un membre !')
            return
        elif not amount:
            await ctx.send('{PREFIX} Veuillez renseigner un montant !')
            return
        elif amount <= 0:
            await ctx.send(f'{PREFIX} Le montant doit être supérieur ou égale à 1 !')
            return
        if (member.id, member.guild.id) in users:
            user = userm.get_user_by_id(member, member.guild)
        else:
            if not userm.exist(member, member.guild):
                await ctx.send('{PREFIX} Cet utilisateur n\'existe pas dans ce serveur !')
                return
            user = userm.load_user(member, member.guild)
        author = userm.load_user(ctx.message.author, ctx.message.author.guild)
        if not userm.exist(author, member.guild):
            await ctx.send(f"{PREFIX} Tu n\'es pas enregistré dans la base de données !")
            return
        if author.superuser or (author.get_id(), author.guild.id) in admins:
            userm.set_xp(user, member.guild, user.get_xp() - amount)
            await ctx.send(f"{PREFIX} a ajouté **{amount}** d\'expériences à {user.get_username() + user.get_discriminator()}, il passe niveau {user.get_level()}")
        else:
            await ctx.send(f"{PREFIX} Tu n'as pas la permission !")

    @commands.command()
    async def setsuperuser(self, ctx, member : discord.Member=None):
        if not member:
            await ctx.send('{PREFIX} Veuillez renseigner un membre !')
            return
        if (member.id, member.guild.id) in users:
            user = userm.get_user_by_id(member, member.guild)
        else:
            if not userm.exist(member, member.guild):
                await ctx.send('{PREFIX} Cet utilisateur n\'existe pas dans ce serveur !')
                return
            user = userm.load_user(member, member.guild)
            author = userm.load_user(ctx.message.author, ctx.message.author.guild)
            if not userm.exist(author, member.guild):
                await ctx.send(f"{PREFIX} Tu n\'es pas enregistré dans la base de données !")
                return
            if not author.superuser:
                await ctx.send(f"{PREFIX} Tu n'as pas la permission !")
                return
        if not user.superuser:
            userm.set_superuser(user)
            await ctx.send(f'{PREFIX} **{user.get_username()}** a été promu au rang de super utilisateur !')
        else:
            await ctx.send(f"{PREFIX} **{user.get_username()}** est déjà super utilisateur !")

def setup(client):
    client.add_cog(AdminCmd(client))