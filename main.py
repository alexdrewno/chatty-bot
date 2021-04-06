import discord
from DiscordClient import DiscordClient
import os

#from dotenv import load_dotenv

#load_dotenv()

# Main script to start the DiscordClient
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

client = DiscordClient()

client.run(DISCORD_TOKEN)
