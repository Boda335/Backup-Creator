import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View, Button
import json
import os
import random
import string

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

def generate_random_code(length=8):
    """Generate a random alphanumeric code."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} commands')
    except Exception as e:
        print(f'Error syncing commands: {e}')

@bot.tree.command(name="backup", description="Create a server template link and save it to a file")
@app_commands.describe(
    privacy="Set the privacy of the backup link (public or private)",
    image1="Optional: URL of the first image to include",
    image2="Optional: URL of the second image to include",
    image3="Optional: URL of the third image to include"
)
@app_commands.choices(privacy=[
    app_commands.Choice(name="Public", value="public"),
    app_commands.Choice(name="Private", value="private")
])
async def backup(interaction: discord.Interaction, privacy: str, image1: str = None, image2: str = None, image3: str = None):
    guild = interaction.guild

    # Ensure the bot has the necessary permissions
    if not guild.me.guild_permissions.manage_guild:
        await interaction.response.send_message("The bot does not have the necessary permissions to manage the server.", ephemeral=True)
        return

    try:
        # Create a server template
        template = await guild.create_template(name=f"{guild.name} Backup", description="Backup of the server's channels and roles")

        # Generate a random code
        random_code = generate_random_code()

        # Prepare the data for storage
        backup_data = {
            "server_name": guild.name,
            "server_id": guild.id,
            "template_url": template.url,
            "privacy": privacy,
            "code": random_code,
            "images": [image1, image2, image3]
        }

        # Remove any None values from the images list
        backup_data["images"] = [img for img in backup_data["images"] if img is not None]

        # The filename to save the data
        filename = "server_backups.json"

        # If the file already exists, load the existing data
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = []

        # Add the current server's data
        data.append(backup_data)

        # Save the data to the file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        # Send the template link to the user without the backup code or image links
        await interaction.response.send_message(f"Backup created! You can restore the server from the following link: {template.url}", ephemeral=True)

    except Exception as e:
        await interaction.response.send_message(f"An error occurred while creating the backup: {e}", ephemeral=True)

class BackupView(View):
    def __init__(self, backups, page=0):
        super().__init__(timeout=60)
        self.backups = backups
        self.page = page
        self.update_buttons()

    def update_buttons(self):
        if self.page == 0:
            self.children[0].disabled = True
        else:
            self.children[0].disabled = False

        if self.page == (len(self.backups) - 1) // 5:
            self.children[1].disabled = True
        else:
            self.children[1].disabled = False

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.primary, custom_id="previous")
    async def previous(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.page > 0:
            self.page -= 1
            self.update_buttons()
            await self.update_embed(interaction)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary, custom_id="next")
    async def next(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.page < (len(self.backups) - 1) // 5:
            self.page += 1
            self.update_buttons()
            await self.update_embed(interaction)

    async def update_embed(self, interaction: discord.Interaction):
        start = self.page * 5
        end = start + 5
        page_backups = self.backups[start:end]

        embed = discord.Embed(title="Public Backups", description="List of public server backups.", color=discord.Color.blue())
        for backup in page_backups:
            embed.add_field(
                name=backup["server_name"],
                value=f"**Server ID:** {backup['server_id']}\n**Backup Code:** {backup['code']}",
                inline=False
            )

        await interaction.response.edit_message(embed=embed, view=self)

@bot.tree.command(name="list_backups", description="List all public server templates with their backup codes")
async def list_backups(interaction: discord.Interaction):
    filename = "server_backups.json"

    # Read the data from the file
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        await interaction.response.send_message("No public backups available.", ephemeral=True)
        return

    # Filter the public backups
    public_backups = [entry for entry in data if entry["privacy"] == "public"]

    if not public_backups:
        await interaction.response.send_message("No public backups available.", ephemeral=True)
        return

    # Send the first page of data
    view = BackupView(public_backups)
    embed = discord.Embed(title="Public Backups", description="List of public server backups.", color=discord.Color.blue())
    start = 0
    end = 5
    page_backups = public_backups[start:end]
    for backup in page_backups:
        embed.add_field(
            name=backup["server_name"],
            value=f"**Server ID:** `{backup['server_id']}`\n**Backup Code:** `{backup['code']}`",
            inline=False
        )

    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

@bot.tree.command(name="restore", description="Get backup information using the backup code")
async def restore(interaction: discord.Interaction, code: str):
    filename = "server_backups.json"

    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        await interaction.response.send_message("No backup data available.", ephemeral=True)
        return

    backup = next((entry for entry in data if entry["code"] == code), None)

    if backup is None:
        await interaction.response.send_message("The backup code is incorrect or does not exist.", ephemeral=True)
        return

    embed = discord.Embed(title=f"Backup Information for Code: {code}", color=discord.Color.blue())
    embed.add_field(name="Server Name", value=backup["server_name"], inline=False)
    embed.add_field(name="Server ID", value=backup["server_id"], inline=False)
    embed.add_field(name="Template URL", value=backup["template_url"], inline=False)
    embed.add_field(name="Privacy", value=backup["privacy"].capitalize(), inline=False)

    if backup["images"]:
        for i, image in enumerate(backup["images"], start=1):
            embed.add_field(name=f"Image {i}", value=image, inline=False)

    await interaction.user.send(embed=embed)
    await interaction.response.send_message("Backup information has been sent to your DMs.", ephemeral=True)

@bot.tree.command(name="delete_backup", description="Delete the backup for the current server")
async def delete_backup(interaction: discord.Interaction):
    filename = "server_backups.json"

    if not os.path.exists(filename):
        await interaction.response.send_message("No backup data available.", ephemeral=True)
        return

    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    updated_data = [entry for entry in data if entry["server_id"] != interaction.guild.id]

    if len(updated_data) == len(data):
        await interaction.response.send_message("No backup found for this server.", ephemeral=True)
        return

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(updated_data, f, ensure_ascii=False, indent=4)

    await interaction.response.send_message("The backup for this server has been deleted.", ephemeral=True)

bot.run('Token')
