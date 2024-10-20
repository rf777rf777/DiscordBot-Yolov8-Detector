import discord
from configs.config import Config
from discord.ext import commands

if __name__ == "__main__":
    config = Config.get_config() 
    intents = discord.Intents.default()
    #需要處理訊息
    intents.message_content = True 
    bot = commands.Bot(intents=intents, command_prefix=config['DISCORD']['PREFIX'])
  
    #定義on_ready event
    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user.name}')
        await bot.load_extension('cogs.commands')
        await bot.load_extension('cogs.events')
  
  
    bot.run(config['DISCORD']['TOKEN'])