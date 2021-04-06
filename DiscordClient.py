import discord
from MongoDB import MongoDB

class DiscordClient(discord.Client):
    """
    Creates an instance of the Bot

    Attributes
    __________
    db: (MongoDB obj)
        Instance of the custom MongoDB class to fetch and update the database

    Functions
    __________
    async on_ready()
        Implementing discord.Client on_ready() that is called when the bot is ready
    async def on_reaction_add(reaction, user)
        Implementing discord.Client on_reaction_add() that is called when a reaction is added to a message
    async on_message(message)
        Implementing discord.Client on_message() that is called when a user messages
        in a server (discord.Guild)

    """
    db = None

    async def on_ready(self):
        """
        Implementing discord.Client on_ready() that is called when the bot is ready

        We do any additional post-initialization set-up here
        """

        print('Logged on as {0}!'.format(self.user))
        self.db = MongoDB()

    async def on_reaction_add(self, reaction, user):
        """
        Implementing discord.Client on_reaction_add() that is called when a reaction is added to a message

        We call the corresponding database method to add that reaction to the message in our database
        """

        self.db.addReactToMessageInDb(reaction)
        
    async def on_message(self, message):
        """
        Implementing discord.Client on_message() that is called when a user messages
        in a server (discord.Guild)

        This is where we add the new message into the database
        """

        if message.author == self.user:
            return

        if len(message.content) < 1:
            return
        
        self.db.addMessageToDb(message)



