import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import os

class Levels(commands.Cog):
    def __init__(self, client):
        self.client = client

        os.chdir(r'C:\Users\Naiman\Documents\Développement\Python\Shina\Shina')

    
    
    
    async def lvl_up(self, user, username):
        current_xp = user['xp']
        current_lvl = user['lvl']

        if current_xp >= round((4 * (current_lvl ** 4)) / 6):
            await self.client.pg_con.execute("UPDATE users SET lvl = $1 WHERE user_id = $2 AND guild_id = $3", current_lvl + 1, user['user_id'], user['guild_id'])   
            return True
        else:
            return False
            

    
    @commands.Cog.listener()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def on_message(self, message):

        if message.author.id == self.client.user.id:
            return

        if message.author.bot:
            return

        author_id = str(message.author.id)
        author_name = message.author.name
        guild_id = str(message.guild.id)

        user = await self.client.pg_con.fetch("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", author_id, guild_id)


        if not user:
            await self.client.pg_con.execute("INSERT INTO users (user_id, guild_id, lvl, xp) VALUES ($1, $2, 1, 0)", author_id, guild_id)

        user = await self.client.pg_con.fetchrow("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", author_id, guild_id)
        await self.client.pg_con.execute("UPDATE users SET xp = $1 WHERE user_id = $2 AND guild_id = $3", user['xp'] + 1, author_id, guild_id)

        if await self.lvl_up(user, message.author):
            await message.channel.send(f"GG {message.author.mention} tu es monté au niveau **{user['lvl'] + 1}** (rt si t kontan)")

        current_xp = user['xp']
        current_lvl = user['lvl']

        if current_lvl >= 10:
            member = message.author
            role = discord.utils.get(member.guild.roles, name="「Loli Hunter」")
            await member.add_roles(role, reason=None)
        if current_lvl >= 20:
            member = message.author
            role = discord.utils.get(member.guild.roles, name="「Lolicops」")
            await member.add_roles(role, reason=None)
        if current_lvl >= 30:
            member = message.author
            role = discord.utils.get(member.guild.roles, name="「Chuunibyô」")
            await member.add_roles(role, reason=None)
        if current_lvl >= 40:
            member = message.author
            role = discord.utils.get(member.guild.roles, name="「Mage Noir」")
            await member.add_roles(role, reason=None)
        if current_lvl >= 50:
            member = message.author
            role = discord.utils.get(member.guild.roles, name="「Passione」")
            await member.add_roles(role, reason=None)
        if current_lvl >= 60:
            member = message.author
            role = discord.utils.get(member.guild.roles, name="「Joestar」")
            await member.add_roles(role, reason=None)
        if current_lvl >= 70:
            member = message.author
            role = discord.utils.get(member.guild.roles, name="「Roi des pirates」")
            await member.add_roles(role, reason=None)

        

    @commands.command()
    async def rank(self, ctx, member : discord.Member = None):
        member = ctx.author if not member else member
        member_id = str(member.id)
        guild_id = str(ctx.guild.id)

        user = await self.client.pg_con.fetch("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", member_id, guild_id)

        if not user:
            await ctx.send('Shina ne trouve pas cet utilisateur dans la liste !')
        else:
            current_xp = user['xp']
            current_lvl = user['lvl']
            embed = discord.Embed(
                color=member.color,
                timestamp=ctx.message.author.created_at
                )
            embed.set_author(name=f'Level - {member}', icon_url=self.client.user.avatar_url)

            embed.add_field(name="Level", value=user[0]['lvl'])
            embed.add_field(name="XP", value=user[0]['xp'])

            await ctx.send(embed=embed)

    @commands.command()
    @has_permissions(administrator=True)
    async def lvlclear(self, ctx, member : discord.Member):
        member = ctx.author if not member else member
        member_id = str(member.id)
        guild_id = str(ctx.guild.id)

        user = await self.client.pg_con.fetch("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", member_id, guild_id)

        if not user:
            await ctx.send('Shina ne trouve pas cet utilisateur dans la liste')
        else:
            user = await self.client.pg_con.fetchrow("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", member_id, guild_id)
            await self.client.pg_con.execute("UPDATE users SET xp = $1 WHERE user_id = $2 AND guild_id = $3", user['xp'] - user['xp'], member_id, guild_id)
            await self.client.pg_con.execute("UPDATE users SET lvl = $1 WHERE user_id = $2 AND guild_id = $3", user['lvl'] - user['lvl'], member_id, guild_id)
            await ctx.send(f'Shina a reset l\'experience et le niveau de **{member.mention}** avec succès !')


    @commands.command()
    @has_permissions(administrator=True)
    async def setlvl(self, ctx, member : discord.Member, lvl : int):
        member = ctx.author if not member else member
        member_id = str(member.id)
        guild_id = str(ctx.guild.id)

        user = await self.client.pg_con.fetch("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", member_id, guild_id)

        if not user:
            await ctx.send('Shina ne trouve pas cet utilisateur dans la liste')
        else:
            user = await self.client.pg_con.fetchrow("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", member_id, guild_id)
            current_xp = user['xp']
            current_lvl = user['lvl']
            await self.client.pg_con.execute("UPDATE users SET xp = $1 WHERE user_id = $2 AND guild_id = $3", user['xp'] - user['xp'], member_id, guild_id)
            await self.client.pg_con.execute("UPDATE users SET lvl = $1 WHERE user_id = $2 AND guild_id = $3", user['lvl'] - user['lvl'], member_id, guild_id)
            await self.client.pg_con.execute("UPDATE users SET xp = $1 WHERE user_id = $2 AND guild_id = $3", user['xp'] + (4 * (lvl ** 4) / 6), member_id, guild_id)
            await self.client.pg_con.execute("UPDATE users SET lvl = $1 WHERE user_id = $2 AND guild_id = $3", user['lvl'] + lvl, member_id, guild_id)
            await ctx.send(f'Shina a mis à jour {member.mention} avec **succès !**')

           


def setup(client):
    client.add_cog(Levels(client))


