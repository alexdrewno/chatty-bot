import discord
from MongoDB import MongoDB

class DiscordClient(discord.Client):
    db = None

    async def on_ready(self):
        """
            Implementing discord.Client on_ready() that is called when the bot is ready

            We do any additional post-initialization set-up here
        """
        print('Logged on as {0}!'.format(self.user))
        self.db = MongoDB()

    async def on_reaction_add(self, reaction, user):
        self.db.addReactToMessageInDb(reaction)
        
    async def on_message(self, message):
        """
        Implementing discord.Client on_message() that is called when a user messages
        in a server (discord.Guild)

        This is where all of the commands are called for the DiscordClient
        """

        if message.author == self.user:
            return

        if len(message.content) < 1:
            return
        
        self.db.addMessageToDb(message)



