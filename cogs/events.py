import discord 
from discord.ext import commands
import datetime
import os, sys
sys.path.append('./')
from Shina import db, calls, running_tasks, EXP_GIVEN_PER_MINUTES
import user
import time
from threading import Thread

class GiveExpTask(Thread):

    def __init__(self, user : user.User):
        Thread.__init__(self)
        self.user = user
        self.running = True

    def run(self):
        while True: 
            running = self.running
            if not running: break
            time.sleep(60)
            self.user.add_xp(self.user.get_xp() + EXP_GIVEN_PER_MINUTES)
            print(f'Shina a ajouté {EXP_GIVEN_PER_MINUTES} d\'expérience à {self.user.get_username()} ! EVENTS.PY')

    def stop(self): 
        self.running = False
        print(f"La tâche de {self.user.get_username()} s'est arrêté. EVENTS.PY")


class Call():

    def __init__(self, user : user.User, started : datetime.datetime) -> None:
        self.user = user
        self.started = started
        self.ended = None

    def get_started_time(self) -> datetime.datetime: return self.started

    def get_ended_time(self) -> datetime.datetime: return self.ended

    def set_ended_time(self, time : datetime.datetime) -> None: self.ended = time

    def commit(self):
        cursor = db.cursor()
        sql = 'INSERT INTO calls(user_id, guild_id, start, end) VALUES(%s, %s, %s, %s)'
        val = (self.user.get_id(), self.user.get_guild_id(), self.get_started_time(), self.get_ended_time())
        cursor.execute(sql, val)
        db.commit()
        print('DEBUG : Un appel a été commit dans la base de données !')
        

class Listener(commands.Cog):

    def __init__(self, client):
        self.client = client

    def create_user(self, member : discord.Member, guild : discord.Guild):
        cursor = db.cursor()
        sql = 'INSERT INTO users(id, guild_id, username, discriminator) VALUES(%s, %s, %s, %s)'
        val = (member.id, guild.id, member.name, member.discriminator)
        cursor.execute(sql, val)
        db.commit()
        print('DEBUG : L\'utilisateur', member.name, ' a été crée dans le serveur', guild.name, '!')

    def end_call(self, member : discord.Member, guild : discord.Guild, date):
        if (member.id, member.guild.id) in calls:
            call = calls[(member.id, member.guild.id)]
            call.set_ended_time(date)
            call_start = call.get_started_time()
            call_end = call.get_ended_time()
            time_elapsed = call_end - call_start
            call_start = call_start.strftime('%Y-%m-%d %H:%M:%S')
            call_end = call_end.strftime('%Y-%m-%d %H:%M:%S')
            call.commit()
            u = user.save_user(member, member.guild)
            running_tasks[(member.id, member.guild.id)].stop()
            del running_tasks[(member.id, member.guild.id)]
            del calls[(member.id, member.guild.id)]
            print(member.name, 'a terminé son appel il a duré', time_elapsed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        date = datetime.datetime.now()
        # print('Membres du channel de apres' + str(after.channel.members))
        # print('Nom du salon de apres' + after.channel.name)
        # print('Membres du channel de avant' + str(before.channel.members))
        # print('Nom du salon de avant' + before.channel.name)
        if after.channel is None or len(after.channel.members) <= 1 or after.channel.id == member.guild.afk_channel.id: # mean if after.channel is AFK channel
            if before.channel is not None and len(before.channel.members) < 2:
                self.end_call(member, member.guild, date)
                for member in before.channel.members:
                    self.end_call(member, member.guild, date)
                return
            self.end_call(member, member.guild, date)
        else:
            if after.channel.id == member.guild.afk_channel.id: return
            for member in after.channel.members:
                if (member.id, member.guild.id) not in calls:
                    if len(after.channel.members) > 1:
                        # self.connections[member.id] = [date, None]
                        print(member.name, 'a rejoint le salon', after.channel.name, 'le', date)
                        if not user.exist(member, member.guild):
                            self.create_user(member, member.guild)
                        u = user.load_user(member, member.guild)
                        call = Call(u, date)
                        calls[(u.get_id(), u.get_guild_id())] = call
                        task = GiveExpTask(u)
                        if (member.id, member.guild.id) not in running_tasks: task.start()
                        running_tasks[(member.id, member.guild.id)] = task
                        print(f'Une tâche de quête d\'expérience vient de se lancer pour {u.get_username()}!')

def setup(client):
    client.add_cog(Listener(client))

