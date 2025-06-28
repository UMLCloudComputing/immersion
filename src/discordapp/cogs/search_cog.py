import botocore.exceptions
from discord.ext import commands
from discord import app_commands
import discord
import boto3
import botocore
from modules.club import Club
from modules.event import Event
from modules.views import *

class SearchCog(commands.GroupCog, name="search", description="Search for clubs or events"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="club", description="Search for a club")
    async def search_club_handler(self, interaction: discord.Interaction, name: str) -> None:
        club_list = await self.get_clubs()
        embed = create_club_embed(club_list[0], 1)
        view = ClubView(results=club_list)
        await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name="event", description="Search for an event")
    async def search_event_handler(self, interaction: discord.Interaction, name: str) -> None:
        event_list = await self.get_events()
        embed = create_event_embed(event_list[0], 1)
        view = EventView(results=event_list)
        await interaction.response.send_message(embed=embed, view=view)
    
    async def get_events(self) -> list[Event]:
        events = []
        # this is where we would actually fetch events from ddb
        for i in range(5):
            events.append(Event(name=f"event{i}", date="1/2/25", time="9:00PM", image_url="https://se-images.campuslabs.com/clink/images/3f63b266-ed37-4070-8678-6aae47084b5008aa61af-5d5d-499e-8c9e-7ed5ce127541.jpeg?preset=med-sq"))
            events.append(Event(name="Immersion coding sesh", date="6/28/25", time="3:00PM", image_url="https://cdn.discordapp.com/avatars/353590230995042314/e9eae59caa9a7ef01dd52ea3c4da3383.webp?size=128"))
        return events
    
    async def get_clubs(self) -> list[Club]:
        clubs = []
        #this is where we would actually fetch clubs from ddb
        ddb = boto3.resource('dynamodb')
        cf = boto3.client('cloudformation')

        resource = None
        table = None
        items = None

        try:
            resource = cf.describe_stack_resource(StackName="ImmersionStack", LogicalResourceId="ImmersionOrganizationTable")
        except botocore.exceptions.ClientError as e:
            print("ERROR! SearchCog::get_clubs():", e)
        else:
            try:
                table = ddb.Table(resource.StackResourceDetail.PhysicalResourceId)
            except Exception as e:
                print("ERROR! SearchCog::get_clubs() raised an Exception:", e)
            else:
                items = table.scan()
        print("Stack resources:", items)




        
        for i in range(5):
            clubs.append(Club(name="Cloud Computing Club", image_url="https://se-images.campuslabs.com/clink/images/3f63b266-ed37-4070-8678-6aae47084b5008aa61af-5d5d-499e-8c9e-7ed5ce127541.jpeg?preset=med-sq"))
        return clubs

async def setup(bot: commands.Bot):
    await bot.add_cog(SearchCog(bot))