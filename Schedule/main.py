import discord
from discord.ext import commands
from command_manager import CommandManager

BOT_TOKEN = ""

client = commands.Bot(command_prefix="-")

async def on_ready():
    print("Ready!")

client.add_listener(on_ready)

cmd_manager = CommandManager(client)
cmd_manager.register_all()
client.run(BOT_TOKEN)
