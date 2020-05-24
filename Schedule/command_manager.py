import discord
from discord.ext import commands
from discord.ext.commands import Command
import datetime
from datahandler import DataHandler

#titan = __import__('/'.join(__file__.split("/")[:-2])+"/utils/titan").Titan()

class TextChannelConverter(commands.TextChannelConverter):
    async def convert(self, ctx, arg):
        return await commands.TextChannelConverter.convert(self, ctx, arg)

class CommandManager():
    def __init__(self, client: discord.Client):
        self.client = client
    def register_all(self):
        # "name" "m/d/y h:m"
        # must check name for quotes
        # check length of name
        # check for duplicates
        # no more than 300 assignments DONE
        @self.client.command()
        async def assign(ctx, name, deadline):
            if len(name) > 300:
                return await ctx.send("Assignment name too long! (Please keep it under 300 characters)")
            if len(name) < 1:
                return await ctx.send("Invalid Assignment name")

            due_date = datetime.datetime.strptime(deadline, '%m/%d/%y %H:%M')
            DataHandler.write(ctx.guild.id, name, due_date)
            await ctx.send(f"Assignment with name \"{name}\" scheduled at {due_date}")

        @assign.error
        async def assign_error(ctx, error):
            print(error)
            await ctx.send("Please follow the syntax `-assign \"Assignment Name\" \"mm/dd/yy hour:minute\"`\nUse \\\\\ to escape \"'s and use 24 hour time")

        @self.client.command()
        async def assignments(ctx):
            data = DataHandler.get(ctx.guild.id)
            if data:
                return await ctx.send('\n'.join(f"\"{x[0]}\"{x[1]}" for x in data if x[0]))
            return await ctx.send("This server is task-clean! :)")
        
        # handle if server file exists or not
        @self.client.command()
        async def complete(ctx, name):
            if DataHandler.remove_task(ctx.guild.id, name):
                return await ctx.send(f"Completed task named {name}")
            return await ctx.send(f"Could not find task named {name}, please see `-assignments` to list pending tasks")




