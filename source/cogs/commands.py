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
        
    @commands.command('di')
    async def d(self, ctx):
        item = ctx.message.attachments[0]
        img_data = await item.read()
        image = Image.open(io.BytesIO(img_data))
        result_stream = yolov8_service().detect_object_info(image, item.filename)
        await ctx.send("Detect 😎：", file=discord.File(fp=result_stream, filename=f'{item.filename}_detected.jpg'))

    @commands.command()
    async def detect(self, ctx):
        #Check attachments
        if not ctx.message.attachments:
            await ctx.send('Please upload a image。')
            return
        
        #All deteect results
        all_detect_result_stream: list[io.BytesIO] = []
        
        for attachment in ctx.message.attachments:
            print(attachment.filename)
            #Check if file is image
            if not attachment.filename.lower().endswith(('png', 'jpg', 'jpeg')):
                continue
            
            await ctx.send(f"Detecting...{attachment.filename}...🔎🔎🔎")
       
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
                await ctx.send(f"{attachment.filename} Object Detect Fail 😓")
                continue  
            
            all_detect_result_stream.append(result_stream)
        
        if len(all_detect_result_stream) <= 0:
            return

        files = [discord.File(fp=stream, filename=f'detected_{i}.jpg') for i, stream in enumerate(all_detect_result_stream)]
        await ctx.send("Detected 😎：", files=files)      
        #await ctx.send("Detect 😎：", file=discord.File(fp=result_stream, filename=f'{attachment.filename}_detected.jpg'))
                
async def setup(bot):
    await bot.add_cog(Commands(bot))