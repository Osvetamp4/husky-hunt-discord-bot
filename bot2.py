import os
from io import BytesIO
import discord
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import httplib2
import auth

load_dotenv("husky.env")
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN is missing from husky.env")

GUILD = os.getenv("GUILD_NAME", "YOUR_DISCORD_SERVER_NAME")

SCOPES = "https://www.googleapis.com/auth/drive"
CLIENT_SECRET_FILE = "client_secret/client_secret_1034602092781-s4kk5o51dhmdgd1lbtiksruu08sopihi.apps.googleusercontent.com.json"
APPLICATION_NAME = "test"

# Get credentials
authInst = auth.auth(SCOPES, CLIENT_SECRET_FILE, APPLICATION_NAME)
credentials = authInst.getCredentials()

# Pass credentials directly to build()
DRIVE_SERVICE = build('drive', 'v3', credentials=credentials)

intents = discord.Intents.default()
intents.message_content = True 

client = discord.Client(intents=intents)

def configured_channel_id(name):
    value = os.getenv(name, "0")
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0

channel_id = configured_channel_id("CHANNEL_ID")
craft_id = configured_channel_id("CRAFT_ID")

def upload_file(parent, drive_service, filename, mimetype, upload_filename, resumable=True): #, chunksize=262144):
        try:
            media = MediaIoBaseUpload(filename, mimetype=mimetype, resumable=resumable) #, chunksize=chunksize)
            # Add all the writable properties you want the file to have in the body!

            request_body = {
                "name": upload_filename,
                "parents": [parent],
            }
            request = drive_service.files().create(body=request_body, media_body=media).execute()
            print("Upload Complete!")
            return True
        except Exception as e:
            print(e)
            return False

@client.event
async def on_ready():
    guild = next((guild for guild in client.guilds if guild.name == GUILD), None)
    print(f'{client.user} has connected to Discord!')
    if guild:
        print(f'{guild.name}(id: {guild.id})')
    else:
        print(f'GUILD_NAME is not configured as a connected server: {GUILD}')

@client.event
async def on_message(message):
    print("Message received")

    if message.author.bot:
        return

    username = message.author.display_name
    guild = message.guild
    if message.channel.id == channel_id or message.channel.id == craft_id:
        bool = False
        if message.attachments:
            for a in message.attachments:
                if a.content_type.startswith("image/") or a.content_type.startswith("video/"):

                    file = BytesIO()
                    await a.save(file)
                    file.seek(0)

                    original_filename = a.filename
                    ext = os.path.splitext(original_filename)[1]

                    new_filename = f"{message.content}{ext}"

                    parent = None

                    # if message.content.startswith("T"):
                    #     print("Message starts with T")
                    #     parent = "1b2WBh4-sIv8KxGTr-XnwBSgId0Bzbd0K"

                    # if message.content.startswith("K"):
                    #     print("Message starts with K")
                    #     parent = "1SAsO7NWNPoLbWdiLGkLJ2VzZGdSfUZoS"

                    if message.content.startswith("A"):
                        parent = "1LgHK0BdtsgR4ugm4YEJu0vEGO-TkIRqS"

                    elif message.content.startswith("B"):
                        parent = "17VgKRdF7mAyMIgH5rI-y5acgohnV5UjB"

                    elif message.content.startswith("C"):
                        parent = "1LdG3Vi-lrLONes22xKv8exOdf6cAwckK"

                    elif message.content.startswith("D"):
                        parent = "1PxHfS4Z6V5cL3A2fzflw31A7dIWPdLUW"

                    elif message.content.startswith("W"):
                        parent = "1SJcovgeO_6NgO4LXDLaRfKiFA5lbs76U"

                    elif message.content.startswith("S"):
                        parent = "1j7Idf_r_peU52DUo7PdmvftFpaEpPSxa"

                    elif message.content.startswith("U"):
                        parent = "16_0VQNS3HRLYqtntuVj6BTnCOCtWh1p1"

                    elif message.content.startswith("Z"):
                        parent = "1gOZ4HoJYQO0j4GeInSjDh3JLElToVUWE"

                    elif message.content.startswith("J"):
                        parent = "1cuR01joObm8KuBQx5HsIbDtwj8XPWmCN"

                    elif message.content.startswith("L"):
                        parent = "1cuR01joObm8KuBQx5HsIbDtwj8XPWmCN"

                    elif message.content.startswith("M"):
                        parent = "1cuR01joObm8KuBQx5HsIbDtwj8XPWmCN"
                    
                    elif message.content.startswith("K"):
                        parent = "1cuR01joObm8KuBQx5HsIbDtwj8XPWmCN"

                    elif message.content.startswith("N"):
                        parent = "1cuR01joObm8KuBQx5HsIbDtwj8XPWmCN"

                    elif message.content.startswith("O"):
                        parent = "1cuR01joObm8KuBQx5HsIbDtwj8XPWmCN"

                    elif message.content.startswith("P"):
                        parent = "1cuR01joObm8KuBQx5HsIbDtwj8XPWmCN"

                    else:
                        return

                    bool = upload_file(parent, DRIVE_SERVICE, file, a.content_type, new_filename)

        if bool:
            await message.reply("Successfully uploaded!")
        else:
            await message.reply("Error uploading attachment")
        
        # await message.delete()

client.run(TOKEN)