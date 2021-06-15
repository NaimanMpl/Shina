from Shina import db, users, admins
import Shina as main
import math
import discord

class User():

    def __init__(self, id, guild_id, username, discriminator, xp, level):
        self.id = id
        self.guild_id = guild_id
        self.username = username
        self.discriminator = discriminator
        self.xp = xp
        self.level = level
        self.superuser = False

    def get_username(self) -> str: return self.username

    def get_discriminator(self) -> int: return self.discriminator

    def get_id(self) -> int: return self.id

    def get_guild_id(self) -> discord.guild: return self.guild_id

    def get_xp(self) -> float: return self.xp

    def set_superuser(self) -> None: self.superuser = True
    
    def get_level(self) -> int: return self.level

    def set_username(self, username) -> None: self.username = username

    def check_level_up(self):
        niveau = (math.sqrt(100 * (2 * self.xp + 25)) + 50) / 100
        if int(niveau) > self.level:
            self.level = int(niveau)
            # main.get_announce_channel().send(f"Félicitations {self.username} tu es monté au niveau {self.level} !")
            print(f"Félicitations {self.username} tu es monté au niveau {self.level} !")

    def add_xp(self, xp) -> None: 
        self.xp = xp
        self.check_level_up()
    
    def set_level(self, level) -> None: self.level = level

    def set_discriminator(self, discriminator) -> None: self.discriminator = discriminator

def get_username(member : discord.Member, guild : discord.Guild) -> str:
    cursor = db.cursor()
    sql = "SELECT username FROM users WHERE id='" + str(member.id) + "' AND guild_id='" + str(guild.id) + "'"
    cursor.execute(sql)
    return cursor.fetchone()[0]

def get_discriminator(member : discord.Member, guild : discord.Guild) -> int:
    cursor = db.cursor()
    sql = "SELECT discriminator FROM users WHERE id='" + str(member.id) + "' AND guild_id='" + str(guild.id) + "'"
    cursor.execute(sql)
    return cursor.fetchone()[0]

def get_xp(member : discord.Member, guild : discord.Guild) -> float:
    cursor = db.cursor()
    sql = "SELECT xp FROM users WHERE id='" + str(member.id) + "' AND guild_id='" + str(guild.id) + "'"
    cursor.execute(sql)
    return cursor.fetchone()[0]

def get_level(member : discord.Member, guild : discord.Guild) -> int:
    cursor = db.cursor()
    sql = "SELECT level FROM users WHERE id='" + str(member.id) + "' AND guild_id='" + str(guild.id) + "'"
    cursor.execute(sql)
    return cursor.fetchone()[0]

def set_discriminator(member : discord.Member, guild : discord.Guild, discriminator : int) -> None:
    cursor = db.cursor()
    sql = "UPDATE users SET discriminator='" + str(discriminator) + "' WHERE id='" + str(member.id) + "' AND guild_id='" + str(guild.id) + "'"
    cursor.execute(sql)
    db.commit()

def set_username(member : discord.Member, guild : discord.Guild, username) -> None:
    cursor = db.cursor()
    sql = "UPDATE users SET username='" + username + "' WHERE id='" + str(member.id) + "' AND guild_id='" + str(guild.id) + "'"
    cursor.execute(sql)
    db.commit()

def set_xp(member : discord.Member, guild : discord.Guild, xp) -> None:
    user = load_user(member, guild)
    user.add_xp(xp)
    print(xp)
    niveau = (math.sqrt(100 * (2 * user.xp + 25)) + 50) / 100
    if int(niveau) > user.level:
        user.level = int(niveau)
    cursor = db.cursor()
    sql = "UPDATE users SET xp='" + str(xp) + "' WHERE id='" + str(member.id) + "' AND guild_id='" + str(guild.id) + "'"
    cursor.execute(sql)
    db.commit()
    set_level(member, guild, niveau)

def set_level(member : discord.Member, guild : discord.Guild, level : int):
    cursor = db.cursor()
    sql = "UPDATE users SET level='" + str(level) + "' WHERE id='" + str(member.id) + "' AND guild_id='" + str(guild.id) + "'"
    cursor.execute(sql)
    db.commit()

def get_calls(member : discord.Member, guild : discord.Guild) -> list:
    cursor = db.cursor()
    sql = "SELECT start, end FROM calls WHERE user_id='" + str(member.id) + "' AND guild_id='" + str(guild.id) + "'"
    cursor.execute(sql)
    return cursor.fetchall()

def get_user_by_id(member : discord.Member, guild : discord.Guild) -> User:
    return users[(member.id, guild.id)]

def superuser(user : User):
    cursor = db.cursor()
    cursor.execute("SELECT id FROM superusers WHERE id='" + str(user.get_id()) + "'")
    response = cursor.fetchone()
    if response is None or response == 0: return False
    return True

def set_superuser(user : User) -> None:
    cursor = db.cursor()
    sql = "INSERT INTO superusers (id, name, discriminator) VALUES(%s, %s, %s)"
    val = (user.get_id(), user.get_username(), user.get_discriminator())
    cursor.execute(sql, val)
    user.superuser = True
    db.commit()

def remove_superuser(user : User) -> None:
    cursor = db.cursor()
    sql = "DELETE FROM superusers WHERE id='" + str(user.get_id()) + "'"
    cursor.execute(sql)
    user.superuser = False
    db.commit()

def admin(user : User, guild : discord.Guild):
    cursor = db.cursor()
    cursor.execute("SELECT user_id FROM admins WHERE id='" + str(user.get_id()) + "' AND guild_id='" + str(guild.id) + "'")
    response = cursor.fetchone()
    if response is None or response == 0: return False
    return True

def set_admin(member : discord.Member, guild : discord.Guild) -> None:
    cursor = db.cursor()
    sql = "INSERT INTO admin VALUES(%s, %s, %s, %s)"
    val = (member.id, guild.id, member.name, member.discriminator)
    cursor.execute(sql, val)
    db.commit()

def remove_admin(member : discord.Member, guild : discord.Guild) -> None:
    cursor = db.cursor()
    sql = "DELETE FROM admin WHERE user_id='" + str(member.id) + "' AND guild_id='" + str(guild.id) + "'"
    cursor.execute(sql)
    del admins[(member.id, guild.id)]
    db.commit()

def load_user(member : discord.Member, guild : discord.Guild) -> User:
    if (member.id, guild.id) not in users:
        username = member.name
        discriminator = member.discriminator
        xp = get_xp(member, guild)
        level = get_level(member, guild)
        user = User(member.id, guild.id, username, discriminator, xp, level)
        if superuser(user): user.superuser = True
        if admin(user, guild): admins[(member.id, guild.id)] = True
        users[(member.id, guild.id)] = user
        if not user.superuser:
            print(f'Les données de l\'utilisateur {username} dans le serveur {guild.name} ont été chargées avec succès !')
        else:
            print(f'Les données du super utilisateur {username} dans le serveur {guild.name} ont été chargées avec succès !')
        return user
    else:
        return users[(member.id, guild.id)]

def create_user(member : discord.Member, guild : discord.Guild):
    cursor = db.cursor()
    sql = 'INSERT INTO users(id, guild_id, username, discriminator) VALUES(%s, %s, %s, %s)'
    val = (member.id, guild.id, member.name, member.discriminator)
    cursor.execute(sql, val)
    db.commit()
    print('DEBUG : L\'utilisateur', member.name, ' a été crée dans le serveur', guild.name, '!')

def save_user(member : discord.Member, guild : discord.Guild) -> User:
    user = get_user_by_id(member, guild)
    set_username(member, guild, user.get_username())
    set_discriminator(member, guild, user.get_discriminator())
    set_xp(member, guild, user.get_xp())
    set_level(member, guild, user.get_level())
    if (member.id, guild.id) in users: del users[(member.id, guild.id)]
    print(f'Les données de l\'utilisateur {user.get_username()} dans le serveur {guild.name} ont été sauvegardées avec succès !')
    return user

def exist(member : discord.Member, guild : discord.Guild) -> bool:
    cursor = db.cursor()
    cursor.execute("SELECT username FROM users WHERE id='" + str(member.id) + "' AND guild_id='" + str(guild.id) + "'")
    response = cursor.fetchone()
    if response is None or response == 0: return False
    return True

def get_xp_from_level(level : int) -> float:
    return (level**2 + level) / 2 * 100 - (level * 100)

def get_level_from_exp(xp : float) -> int:
    return int((math.sqrt(100 * (2 * xp + 25)) + 50) / 100)