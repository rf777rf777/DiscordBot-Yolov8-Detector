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
        
    @commands.command('d')
    async def detect(self, ctx):
        #Check attachments
        if not ctx.message.attachments:         
            await ctx.send(embed=self.__getMessageEmbed(f"Please upload an image."))
            return
        
        all_detect_result_stream: list[io.BytesIO] = []
        for item in ctx.message.attachments:
            if not self.__isImageFile(item.filename):
                continue
            await ctx.send(embed=self.__getMessageEmbed(f"{item.filename}: Detecting"))
            
            #Read image data
            img_data = await item.read()

            #Get PIL image
            try:                      
                image = Image.open(io.BytesIO(img_data))
            except:    
                await ctx.send(embed=self.__getMessageEmbed(f"{item.filename}: Get PIL error", "⛔"))    
                continue

            result_stream = yolov8_service().detect_object_info(image, item.filename)
            if result_stream is None:
                await ctx.send(embed=self.__getMessageEmbed(f"{item.filename}: Detected nothing", "😓"))
                continue  

            all_detect_result_stream.append(result_stream)

        if len(all_detect_result_stream) <= 0:
            return

        files = [discord.File(fp=stream, filename=f'detected_{i}.jpg') for i, stream in enumerate(all_detect_result_stream)]
        await ctx.send(embed=self.__getMessageEmbed("Detected", "😎"), files=files)   

        
    def __isImageFile(self, filename:str) -> bool:
        if filename.lower().endswith(('png', 'jpg', 'jpeg')):
          return True
        return False
      
    def __getMessageEmbed(self, message:str, icon:str="🔊") -> discord.Embed:
        return discord.Embed(
            description=f"{icon} {message}",
            color=discord.Color.from_rgb(184, 134, 11)
        )

async def setup(bot):
    await bot.add_cog(Commands(bot))