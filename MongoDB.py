from pymongo import MongoClient
import os
from datetime import datetime

#from dotenv import load_dotenv

#load_dotenv()

class MongoDB: 

    def __init__ (self):
        self.client = MongoClient(os.getenv('MONGO_URI'))
        self.db = self.client.ChatLogs
    
    def addMessageToDb(self, message):
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
        messageDict = self.db.logs.find_one({"_id": reaction.message.id})

        if reaction.custom_emoji:
            messageDict["reactions"].append(reaction.emoji.name)
        else:
            messageDict["reactions"].append(reaction.emoji)

        myQuery = { "_id": reaction.message.id }
        updatedReactions = { "$set": { "reactions": messageDict["reactions"] } }

        self.db.logs.update_one(myQuery, updatedReactions)
    