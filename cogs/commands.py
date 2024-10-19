import discord
from discord.ext import commands
#from modules.pagination_view import PaginationView
#from modules.instagram_item import InstagramItem
import re
import requests
import io


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #self.ig_item = InstagramItem('yuzuki_yzk030')
        #self.ig_item = InstagramItem('momiko_124')
        #self.ig_item = InstagramItem('eeelyeee')
        #self.ig_item = InstagramItem('walkerpretty96')
        #self.ig_item = InstagramItem('mei.x.mei')

        #self.profile = ig_item.get_user_profile()
        # self.latest_post = None
        # self.profile = None

    @commands.command()
    async def hello(self, ctx):
        await ctx.send('Hello from command!')

    @commands.command()
    async def ig(self, ctx):
        # 檢查該消息是否包含附件
        if not ctx.message.attachments:
            await ctx.send('請上傳一張圖片作為附件。')
            return
        
        for attachment in ctx.message.attachments:
            # 確認文件是圖片
            if not attachment.filename.lower().endswith(('png', 'jpg', 'jpeg')):
                continue
            # 下載附件的數據
            img_data = await attachment.read()
                    
                    
            # 使用 BytesIO 將圖片轉換為類文件對象，便於上傳
            #image_stream = io.BytesIO(img_data)
            #image_stream.seek(0)  # 確保文件指針回到起點

            # 構建多部分表單數據的上傳請求
            files = {'file': (attachment.filename, img_data, 'multipart/form-data')}
            response = requests.put('http://45.130.166.218:8000/Detection/Image', files=files)
            
            if response.status_code != 200:
                await ctx.send(f"圖片上傳失敗，狀態碼：{response.status_code}")
                await ctx.send(f'已處理圖片檔案：{attachment.filename}')
                continue               
            
            # 確保請求成功
            if response.status_code == 200:
                # 如果回應中包含文件（例如處理後的圖片）
                response_file_data = response.content  # 假設回應是二進制的文件數據

                # 將回應的文件作為附件發送回 Discord
                response_image_stream = io.BytesIO(response_file_data)
                response_image_stream.seek(0)
                response_filename = 'response_image.png'  # 根據需要設置回應文件的名稱
                response_file = discord.File(fp=response_image_stream, filename=response_filename)
                await ctx.send("已接收處理後的圖片：", file=response_file)
        else:
            await ctx.send('請上傳一張圖片作為附件。')
        # ig_item = InstagramItem(username)
        # profile = ig_item.get_user_profile()
        # latest_post = ig_item.get_latest_post()
        # view = PaginationView(total_items=len(latest_post.post_items), update_embed_callback=self.generate_embed, profile=profile, latest_post=latest_post)
        # embed = self.generate_embed(0, profile, latest_post)
        # caption = latest_post.caption or ''      
        # caption = re.sub(r'#\w+', '', caption).strip()
        # if len(caption) > 100:
        #     caption = f'{caption[:100]} ... [<詳見貼文>](https://www.instagram.com/p/{latest_post.code})'
        # await ctx.send(embeds=[embed, embed]) #複數個影像
async def setup(bot):
    await bot.add_cog(Commands(bot))