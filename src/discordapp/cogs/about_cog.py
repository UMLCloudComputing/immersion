from discord.ext import commands
from discord.ext import app_commands
import discord
class AboutCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="about")
    async def about_handler(self, interaction: discord.Interaction):
        embed = create_about_embed()
        await interaction.response.send_message(embed=embed)







async def setup(bot: commands.Bot):
    await bot.add_cog(AboutCog(bot))