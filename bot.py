import os
from io import BytesIO
import discord
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

load_dotenv("husky.env")
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN is missing from husky.env")

GUILD = None # REPLACE WITH SERVER

creds = service_account.Credentials.from_service_account_file(
    "service.json",
    scopes=["https://www.googleapis.com/auth/drive"]
)
drive_service = build("drive", "v3", credentials=creds)

intents = discord.Intents.default()
intents.message_content = True 

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print(f'{client.user} has connected to Discord!')
    print(f'{guild.name}(id: {guild.id})')

@client.event
async def on_message(message):
    print("Message received")

    if message.author.bot:
        return

    username = message.author.display_name
    guild = message.guild
    image_channel = guild.get_channel(1441268591205814292)
    if message.attachments:
        for a in message.attachments:
            if a.content_type.startswith("image/"):

                file = BytesIO()
                await a.save(file)
                file.seek(0)

                original_filename = a.filename
                ext = os.path.splitext(original_filename)[1]

                new_filename = f"{message.content}{ext}"

                print("Service account email:", creds.service_account_email)

                file_metadata = {
                    "name": new_filename,
                    "parents": ["1-BLO-srp2t26hMLMHxOjS5DsOAeoUExm"]
                }

                media = MediaIoBaseUpload(file, mimetype=a.content_type)

                uploaded = drive_service.files().create(
                    body=file_metadata,
                    media_body=media,
                    fields="id"
                ).execute()

                await message.channel.send(f"Uploaded to Google Drive with ID: {uploaded['id']}")
        await message.delete()

client.run(TOKEN)