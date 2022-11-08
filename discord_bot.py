from discord.errors import ClientException, Forbidden
from models.disc_gui import discordBook
import discord
import asyncio
import os

class AssettoStatsBot(discord.Client):

    def __init__(self, intents):
        self.directory = os.path.dirname(__file__)
        self.servers = []

        super().__init__(intents = intents)



    async def on_message(self, message):
        print("MESSAGE RECEIVED")

        async def add_song(server, message):
            server.add(message.content, message.author)
            if not server.is_playing():
                await self.handle_play_pause(server, message.author)

        if message.author == client.user:
            return
        server = self.get_server_from_channel_id(message.channel.id)
        if server:
            if message.channel.id == server.get_channel_id():
                await asyncio.sleep(0.5)
                await message.delete()
                if server.vc:
                    if server.is_member_in_call(message.author):
                        await add_song(server, message)

                else:
                    if server.is_member_connected(message.author):
                        await add_song(server, message)

    async def on_raw_message_delete(self, payload):
        print("on_raw_message_delete")
        message_id = payload.message_id
        channel_id = payload.channel_id
        
        server = self.get_server_from_channel_id(channel_id)
        guild = client.get_guild(server.id)


        server_message_id = server.book.message.id
        if server_message_id == message_id:
            self.servers.remove(server)
            await asyncio.sleep(5)
            await self._setup_guild(guild)
    



    async def on_ready(self):
        for guild in client.guilds:
            await self._setup_guild(guild)
        
        print("Bot Online!")
        print("Name: {}".format(self.user.name))
        print("ID: {}".format(self.user.id))
        print("Version: {}".format(discord.__version__))
        print(discord.opus.is_loaded())

    #Respond to reacts to the message
    async def on_raw_reaction_add(self, payload:discord.RawReactionActionEvent):
        member = payload.member
        emoji = payload.emoji
        message_id = payload.message_id
        channel_id = payload.channel_id
        if client.user == member:
            return

        server = self.get_server_from_channel_id(channel_id)
        if server:
            book = server.book
            result = await book.handle_react(emoji, member, message_id)
            
        else:
            result = -1


        if result == -1:
            return
        
        elif result == 1:
            await server.to_start()

        elif result == 2:
            await server.previous_audio()

        elif result == 3:
            await self.handle_play_pause(server, member)
        
        elif result == 4:
            await server.next_audio()

        elif result == 5:
            await server.to_end()
            
        elif result == 6:
            server.remove_song(server.current)

        elif result == 7:
            await server.stop_audio()

        print("React result ", result)

    async def on_voice_state_update(self, member, before, after):
        if before.channel:
            server = self.get_server_from_id(before.channel.guild.id)
            if server:
                if server.is_bot_alone():
                    await server.stop_audio()




def get_token():
    with open("data/discordToken.txt", "r") as f:
        token = f.readline()
        return token


if __name__ == "__main__":
    intents = discord.Intents.all()
    
    client = MusicBot(intents=intents)
    client.run(get_token())

#Stop Button
#