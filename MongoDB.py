from pymongo import MongoClient
import os
from datetime import datetime

#from dotenv import load_dotenv

#load_dotenv()

class MongoDB: 
    """
    Creates an instance of the MongoDB database

    Attributes
    __________
    db: (MongoDB obj)
        The collection where we are storing our data in the MongoDB database

    Functions
    __________
    addMessageToDb(message)
        Add a new message to the database
    addReactToMessageInDb(reaction)
        Add a new reaction to an existing message in the database
    """

    def __init__ (self):
        self.client = MongoClient(os.getenv('MONGO_URI'))
        self.db = self.client.ChatLogs
    
    def addMessageToDb(self, message):
        """
        Add a new message to the database

        Parameters
        ----------
        message : discord.Message
            The message object that we want to get info from and add to our database
        """

        messageDict = {
            "_id": message.id,
            "date": datetime.utcnow().isoformat(),
            "authorName": message.author.name,
            "authorDiscriminator": message.author.discriminator,
            "guild": message.guild.name,
            "channel": message.channel.name,
            "reactions": [],
            "message": message.content,
        }

        self.db.logs.insert_one(messageDict)

    def addReactToMessageInDb(self, reaction):
        """
        Add a new reaction to an existing message in the database

        Parameters
        ----------
        reaction : discord.reaction
            The reaction object that we want to get info from and add to a message in our database
        """

        messageDict = self.db.logs.find_one({"_id": reaction.message.id})

        if reaction.custom_emoji:
            messageDict["reactions"].append(reaction.emoji.name)
        else:
            messageDict["reactions"].append(reaction.emoji)

        myQuery = { "_id": reaction.message.id }
        updatedReactions = { "$set": { "reactions": messageDict["reactions"] } }

        self.db.logs.update_one(myQuery, updatedReactions)
    