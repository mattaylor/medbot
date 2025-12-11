import discord
import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
API_URL = os.getenv("API_URL", "http://localhost:8000")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!ask'):
        query = message.content[5:].strip()
        if not query:
            await message.channel.send("Please provide a query.")
            return

        try:
            response = requests.post(f"{API_URL}/query", json={"text": query})
            response.raise_for_status()
            answer = response.json().get("response", "No response from agent.")
            await message.channel.send(answer)
        except Exception as e:
            await message.channel.send(f"Error: {str(e)}")

if __name__ == "__main__":
    if not TOKEN:
        print("Error: DISCORD_TOKEN not found in environment variables.")
    else:
        client.run(TOKEN)
