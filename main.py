import discord
from discord.ext import commands
import json
import re
import asyncio
description = 'Auto reaction bot'

with open("./settings.json", "r") as f:
    settings = json.load(f)
    
prefix = settings['prefix']
token = settings['token']

class AutoReactBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=prefix, description=description, self_bot=True)
        self.auto_react_enabled = False
        self.reaction = None
        self.active_channel = None
        self.self_react = False
        self.user_reactions = {}
        self.add_commands()

    def is_valid_emoji(self, reaction_str):
        try:
            return True if discord.PartialEmoji.from_str(reaction_str) else False
        except:
            return False

    def add_commands(self):
        @self.command(name="autoreact", description="Enables Autoreactions", aliases=['ar'])
        async def autoreact(ctx, reaction: str, user: discord.Member = None):
            reaction = reaction.split('<@')[0].strip()
            
            if not self.is_valid_emoji(reaction):
                await ctx.send("That's not a valid Discord emoji! Try again with a proper emoji.")
                return

            self.auto_react_enabled = True
            self.active_channel = ctx.channel.id
            
            if user:
                self.user_reactions[user.id] = reaction
                await ctx.send(f"Auto-react enabled for {user.name} with reaction: {reaction} in this channel")
            else:
                self.reaction = reaction
                await ctx.send(f"Auto-react enabled with reaction: {reaction} in this channel")

        @self.command(name="stopreact", description="Disables Autoreactions", aliases=['sr'])
        async def stopreact(ctx, user: discord.Member = None):
            if user:
                if user.id in self.user_reactions:
                    del self.user_reactions[user.id]
                    await ctx.send(f"Auto-react disabled for {user.name}")
            else:
                self.auto_react_enabled = False
                self.reaction = None
                self.active_channel = None
                self.self_react = False
                self.user_reactions.clear()
                await ctx.send("Auto-react disabled for everyone")

        @self.command(name="selfreact", description="Toggle reacting to your own messages", aliases=['selfr'])
        async def selfreact(ctx):
            self.self_react = not self.self_react
            status = "enabled" if self.self_react else "disabled"
            await ctx.send(f"Self-reactions {status}")

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, message):
        await self.process_commands(message)
        if message.author.bot:
            return

        if self.auto_react_enabled and message.channel.id == self.active_channel:
            if message.author.id in self.user_reactions:
                reaction_to_use = self.user_reactions[message.author.id]
                try:
                    await asyncio.sleep(0.5)
                    await message.add_reaction(reaction_to_use)
                except discord.errors.HTTPException:
                    print(f"Failed to react with {reaction_to_use}")
                return
                
            if self.reaction and (message.author.id != self.user.id or self.self_react):
                try:
                    await message.add_reaction(self.reaction)
                except discord.errors.HTTPException:
                    print(f"Failed to react with {self.reaction}")
bot = AutoReactBot()
bot.run(token)