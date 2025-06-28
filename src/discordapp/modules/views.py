import discord
from modules.event import Event
from modules.club import Club

class EventView(discord.ui.View):
    def __init__(self, results: list[Event]):
        super().__init__()
        self.results = results
        self.current_result = 0
    
    @discord.ui.button(label="Previous", style=discord.ButtonStyle.primary)
    async def prev_result_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_result > 0:
            self.current_result -= 1
            embed = create_event_embed(self.results[self.current_result], self.current_result + 1)
            await interaction.response.edit_message(embed=embed)
        else:
            await interaction.response.send_message(ephemeral=True, content="No more results", delete_after=3)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.green)
    async def next_result_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_result < len(self.results) - 1:
            self.current_result += 1
            embed = create_event_embed(self.results[self.current_result], self.current_result + 1)
            await interaction.response.edit_message(embed=embed)
        else:
            await interaction.response.send_message(ephemeral=True, content="No more results", delete_after=3)
    
    #TODO: engage button
    # @discord.ui.button(label="Engage", style=discord.ButtonStyle.link)
    # async def engage_button(self, interaction: discord.Interaction, button: discord.ui.Button):
    #     await interaction.response.send_message("Not implemented!")

class ClubView(discord.ui.View):
    def __init__(self, results: list[Club]):
        super().__init__()
        self.results = results
        self.current_result = 0

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.primary)
    async def prev_result_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_result > 0:
            self.current_result -= 1
            embed = create_club_embed(self.results[self.current_result], self.current_result + 1)
            await interaction.response.edit_message(embed=embed)
        else:
            await interaction.response.send_message(ephemeral=True, content="No more results", delete_after=3)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.green)
    async def next_result_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_result < len(self.results) - 1:
            self.current_result += 1
            embed = create_club_embed(self.results[self.current_result], self.current_result + 1)
            await interaction.response.edit_message(embed=embed)
        else:
            await interaction.response.send_message(ephemeral=True, content="No more results", delete_after=3)

class AboutView(discord.ui.View):
    def __init__(self, name: str):
        self.name = name
        

def create_event_embed(event: Event, idx: int) -> discord.Embed:
    embed = discord.Embed(title=f"Search result {idx}:")
    embed.add_field(name="Name", value=event.name)
    embed.add_field(name="Date", value=event.date)
    embed.add_field(name="Time", value=event.time)
    embed.set_image(url=event.image_url)
    return embed

def create_club_embed(club: Club, idx: int) -> discord.Embed:
    embed = discord.Embed(title=f"Search result {idx}:")
    embed.add_field(name="Name", value=club.name)
    embed.set_image(url=club.image_url)
    return embed