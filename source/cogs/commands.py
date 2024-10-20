import discord
from discord.ext import commands
#from modules.pagination_view import PaginationView
#from modules.instagram_item import InstagramItem
import re
import requests
import io
from PIL import Image

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
        
            # 顯示正在輸入的狀態
        await ctx.typing()            
        for attachment in ctx.message.attachments:
                print(attachment.filename)
                # 確認文件是圖片
                if not attachment.filename.lower().endswith(('png', 'jpg', 'jpeg')):
                    continue
                # 下載附件的數據
                img_data = await attachment.read()
                        
                        
                # 使用 BytesIO 將圖片轉換為類文件對象，便於上傳
                #image_stream = io.BytesIO(img_data)
                #image_stream.seek(0)  # 確保文件指針回到起點

                image = Image.open(io.BytesIO(img_data))

                # 初始化 BytesIO 以保存壓縮後的圖片
                output = io.BytesIO()

                while True:
                    # 清空 BytesIO 並重新保存圖片，質量為 90%
                    output.seek(0)
                    image.save(output, format='JPEG', quality=90)

                    # 檢查圖片的大小
                    file_size = output.tell()  # `tell()` 返回的是文件的當前大小，BytesIO 模擬文件對象

                    if file_size <= 200 * 1024:  # 如果文件大小小於或等於 200KB，停止壓縮
                        break
                    else:
                        # 每次固定壓縮質量，並將圖片再次壓縮
                        # 縮小圖片的尺寸以達到進一步的壓縮
                        width, height = image.size
                        new_size = (int(width * 0.9), int(height * 0.9))  # 每次縮小 90%
                        image = image.resize(new_size, Image.Resampling.LANCZOS) 
                # 重置 BytesIO 的指針
                output.seek(0)


                # 構建多部分表單數據的上傳請求
                files = {'file': (attachment.filename, output, 'multipart/form-data')}
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
                    response_filename = 'response_image.jpg'  # 根據需要設置回應文件的名稱
                    response_file = discord.File(fp=response_image_stream, filename=response_filename)
                    await ctx.send("已接收處理後的圖片：", file=response_file)
            # ig_item     = InstagramItem(username)
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