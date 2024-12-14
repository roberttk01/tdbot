import discord
import openai
import random
import json

# Load configuration from file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Initialize the Discord client
client = discord.Client()

# Initialize OpenAI API
openai.api_key = config['openai_api_key']

# Load truth and dare data
def load_data():
    with open('questions.json', 'r') as f:
        data = json.load(f)
    return data['truths'], data['dares']

truths, dares = load_data()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith('!truth'):
        await message.channel.send(random.choice(truths))

    elif message.content.lower().startswith('!dare'):
        await message.channel.send(random.choice(dares))

    elif message.content.lower().startswith('!askchatgpt'):
        prompt = message.content[len('!askchatgpt '):]
        if prompt:
            response = openai.Completion.create(
                model="gpt-4",  # Use GPT-4 or GPT-3.5 depending on your access
                prompt=prompt,
                max_tokens=50
            )
            await message.channel.send(response.choices[0].text.strip())
        else:
            await message.channel.send("Please provide a question or prompt for ChatGPT.")

client.run(config['discord_token'])
