import discord
from discord.ext import commands
import io
from PIL import Image
from modules.yolov8_service import yolov8_service

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send('Hello from command!')

    @commands.command()
    async def detect(self, ctx):
        #Check attachments
        if not ctx.message.attachments:
            await ctx.send('Please upload a image。')
            return
        
        #To show bot is typing
        await ctx.typing()            
        for attachment in ctx.message.attachments:
            print(attachment.filename)
            #Check if file is image
            if not attachment.filename.lower().endswith(('png', 'jpg', 'jpeg')):
                continue
            #Read data as bytes
            img_data = await attachment.read()

            #Get PIL Image
            try:                      
                image = Image.open(io.BytesIO(img_data))
            except:                  
                print('Get PIL error!')
                continue
                
            result_stream = yolov8_service().detect_object(image, attachment.filename)
            
            if result_stream is None:
                await ctx.send(f"Object Detect Fail 😓")
                continue  
                         
            await ctx.send("Detect 😎：", file=discord.File(
                fp=result_stream, 
                filename=f'{attachment.filename}_detected.jpg'))
     
                
async def setup(bot):
    await bot.add_cog(Commands(bot))