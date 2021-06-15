import discord
from discord.ext import commands
import sys
sys.path.append('./')
from datetime import timedelta
from Shina import db, users
import user as userm
from PIL import Image, ImageDraw, ImageFont
import io
import numpy as np

def crop_image_circular(img : Image) -> Image:
    npImg = np.array(img)
    height, weight = img.size
    alpha = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([0, 0, height, weight], 0, 360, fill=255)
    npAlpha = np.array(alpha)
    npImg = np.dstack((npImg, npAlpha))
    output = Image.fromarray(npImg)
    return output

def generate_mask(img : Image) -> Image:
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + img.size, fill=255)
    return mask

def import_users_from_guild(guild : discord.Guild) -> list:
    cursor = db.cursor()
    sql = f"SELECT id, username, discriminator, xp, level FROM users WHERE guild_id='{guild.id}'" 
    cursor.execute(sql)
    return cursor.fetchall()

def takeXP(guild_users : list):
    return guild_users[3]

class UsersCmd(commands.Cog):

    def __init__(self, client):
        self.client = client

    def create_user(self, member : discord.Member, guild : discord.Guild):
        cursor = db.cursor()
        sql = 'INSERT INTO users(id, guild_id, username, discriminator) VALUES(%s, %s, %s, %s)'
        val = (member.id, guild.id, member.name, member.discriminator)
        cursor.execute(sql, val)
        db.commit()
        print('DEBUG : L\'utilisateur', member.name, ' a été crée dans le serveur', guild.name, '!')

    @commands.command()
    async def stats(self, ctx, member : discord.Member=None):
        if not member:
            member = ctx.message.author
        if (member.id, member.guild.id) in users:
            user = userm.get_user_by_id(member, member.guild)
        else:
            if not userm.exist(member, member.guild):
                self.create_user(member, member.guild)
            user = userm.load_user(member, member.guild)
        time_elapsed = timedelta(0, 0, 0, 0, 0, 0)
        for call in userm.get_calls(member, member.guild):
            call_time = call[1] - call[0]
            time_elapsed = time_elapsed + call_time
        await ctx.send(f"{user.get_username()} a passé {time_elapsed} en appel sur {member.guild.name}.")
        lvl = user.get_level() + 1
        xp_for_lvlup = (lvl**2 + lvl) / 2 * 100 - (lvl * 100)
        await ctx.send(f"{user.get_username()} a actuellement {user.get_xp()}/**{xp_for_lvlup}** et est niveau {user.get_level()}")

    @commands.command()
    async def canvas(self, ctx, member : discord.Member=None):
        if not member:
            member = ctx.message.author
        if (member.id, member.guild.id) in users:
            user = userm.get_user_by_id(member, member.guild)
        else:
            if not userm.exist(member, member.guild):
                self.create_user(member, member.guild)
            user = userm.load_user(member, member.guild)
        
        WIDTH = 982
        HEIGHT = 282
        AVATAR_SIZE = 256

        avatar_asset = member.avatar_url_as(format='png', size=AVATAR_SIZE)
        
        buffer_avatar = io.BytesIO()
        await avatar_asset.save(buffer_avatar)
        buffer_avatar.seek(0)

        avatar_image = Image.open(buffer_avatar).convert('RGB')
        avatar_image = avatar_image.resize((180, 180))
        avatar_x = 42
        avatar_y = (HEIGHT - 180) // 2

        img = Image.new('RGB', (WIDTH, HEIGHT), color='#2c2f33')
        draw = ImageDraw.Draw(img)
        draw.rectangle([30, 30, WIDTH-30, HEIGHT-30], fill=(20, 20, 20))
        
        username = user.get_username()
        discriminator = '#' + str(user.get_discriminator())
        rank_text = 'RANK'
        guild_users = import_users_from_guild(member.guild)
        guild_users.sort(key=takeXP, reverse=True)
        rank = 'None'
        for guild_user in guild_users:
            if guild_user[0] == member.id:
                rank = '#' + str(guild_users.index(guild_user) + 1)
        level_text = 'LEVEL'
        level = str(user.get_level())
        xp = str(user.get_xp())
        xp_for_lvlup = str(userm.get_xp_from_level(user.get_level() + 1))


        font = ImageFont.truetype('./fonts/BloggerSans-Bold.ttf', size=35)
        thin_font = ImageFont.truetype('./fonts/BloggerSans-Light.ttf', size=30)

        text_width, text_height = draw.textsize(username, font=font)
        x = (WIDTH - text_width) // 2
        middle_y = (HEIGHT - text_height) // 2

        # MIDDLE INFORMATIONS

        USERNAME_X = (avatar_x + 250)
        DISCRIMINATOR_X = USERNAME_X + len(username)**2 + 70
        XP_X = DISCRIMINATOR_X + 180
        SLASH_X = XP_X + len(str(xp) + '.0')**2 + 40
        XP_FOR_LVLUP_X = SLASH_X + 40
        RANK_TEXT_X = HEIGHT + 400
        RANK_X = RANK_TEXT_X + 70
        LEVEL_TEXT_X = RANK_TEXT_X + 150
        LEVEL_X = LEVEL_TEXT_X + 80
        TOP_Y = middle_y - 65

        draw.text((RANK_TEXT_X, TOP_Y), rank_text, fill='#FFFFFF', font=thin_font)
        draw.text((RANK_X, TOP_Y), rank, fill='#FFFFFF', font=thin_font)
        draw.text((LEVEL_TEXT_X, TOP_Y), level_text, fill='#CA99FF', font=thin_font)
        draw.text((LEVEL_X, TOP_Y), level, fill='#CA99FF', font=thin_font)
        

        draw.text((USERNAME_X, middle_y), username, fill='#FFFFFF', font=font)
        draw.text((DISCRIMINATOR_X, middle_y + 5), discriminator, fill='#9BABB8', font=thin_font)
        draw.text((XP_X, middle_y), xp, fill='#FFFFFF', font=font)
        draw.text((SLASH_X, middle_y), ' / ', fill='#FFFFFF', font=font)
        draw.text((XP_FOR_LVLUP_X, middle_y), xp_for_lvlup, fill='#FFFFFF', font=font)

        mask = generate_mask(avatar_image)
        img.paste(avatar_image, (avatar_x, avatar_y), mask)

        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)

        await ctx.send(file=discord.File(buffer, 'card.png'))

    @commands.command()
    async def leaderboard(self, ctx):
        member = ctx.message.author
        await ctx.send(f'Classement des utilisateurs de {member.guild.name}\n')
        guild_users = import_users_from_guild(member.guild)
        guild_users.sort(key=takeXP, reverse=True)
        for i in range(5):
            user = guild_users[i]
            rank = guild_users.index(user) + 1
            username = user[1].decode()
            discriminator = user[2]
            xp = user[3]
            level = user[4]
            await ctx.send(f"**#{rank} {username}#{discriminator}** - Niveau : **{level}**, Expérience : **{xp}**\n")
        

def setup(client):
    client.add_cog(UsersCmd(client))
            
    