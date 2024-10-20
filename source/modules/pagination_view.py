import discord

class PaginationView(discord.ui.View):
    def __init__(self, total_items, update_embed_callback, profile, latest_post, index=0):
        super().__init__()
        self.index = index
        self.profile = profile
        self.latest_post = latest_post
        self.total_items = total_items
        self.update_embed_callback = update_embed_callback
        
        if total_items <= 1:
            self.clear_items()
        else:
            # 根據當前 index 設定按鈕狀態
            self.previous.disabled = self.index == 0
            self.next.disabled = self.index == self.total_items - 1
        
    @discord.ui.button(label="Previous", style=discord.ButtonStyle.blurple)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.index > 0:
            self.index -= 1
        await self.update_buttons()
        await self.update_embed(interaction)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.blurple)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.index < self.total_items - 1:
            self.index += 1
        await self.update_buttons()
        await self.update_embed(interaction)

    async def update_buttons(self):
        # 根據 index 禁用按鈕
        self.previous.disabled = self.index == 0
        self.next.disabled = self.index == self.total_items - 1

    async def update_embed(self, interaction: discord.Interaction):
        embed = self.update_embed_callback(self.index, self.profile, self.latest_post)  # 使用回調函數更新 embed
        await interaction.response.edit_message(embed=embed, view=self)
