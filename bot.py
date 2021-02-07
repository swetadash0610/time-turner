import os
import re
import discord
import asyncio
from datetime import datetime
from dotenv import load_dotenv
import pymongo
import wtftz
from pymongo import MongoClient
import urllib
from timeZone import UTC_offset
from convertTime import convertTime

cluster = MongoClient("mongodb+srv://shivanshu:" + urllib.parse.quote("Khusi@123") + "@cluster0.qzsh9.mongodb.net/test")
db = cluster["time-turner"]
collection = db["time-turner"]

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
client = discord.Client(intents=intents)

# On succesfull connecting to a guild
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

# When the bot newly joins a guild 
@client.event
async def on_guild_join(guild):
    for member in guild.members:# for all the members in the server when the bot joins
        try:
            await member.create_dm()# create a dm 
            embedVar = discord.Embed(title="Hi {member.name}", description="Welcome to {guild.name}", color=0x00ff00)#the embed message
            await member.dm_channel.send(embed=embedVar)#send the message
            def check(message):#checks if the user replied
                return message.author.id==member.id
            msg = await client.wait_for('message',check=check)
            reply=msg.content#obstain the content of user reply
            print(reply)
            post= {"user_id": member.id, "guild_id":guild.id,"timezone": reply}
            collection.insert_one(post)#post it in database
        except:
            pass

# On addition of a new member to the server 
@client.event
async def on_member_join(member):
    # member_id = member.id
    await member.create_dm()
    embedVar = discord.Embed(title="Hi", description="Yes khela", color=0x00ff00)
    await member.dm_channel.send(embed=embedVar)
    def check(message):
        return message.author.id==member.id
    msg = await client.wait_for('message',check=check)
    reply=msg.content
    print(reply)
    post= {"user_id": member.id, "guild_id":member.guild.id,"timezone": reply}
    collection.insert_one(post)

# On receiving a message in the guild
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    else:
        content = message.content.lower() #obtain the content of message sent in channel
        content=re.sub('[^A-Za-z0-9: ]+', '', content) #remove special characters
        content = re.findall(r"[^\W\d_]+|\d+(?::\d+)?", content) #separate the string at spaces and numbers
        print(content)
        print(UTC_offset(content[0]))
        # timeutc= message.created_at
        # timeutc= timeutc.strftime("%Y-%m-%dT%H:%M:%S.%f %Z")
        # print(timeutc)

        if any(item in ["am","pm"] for item in content): #if am or pm is found in the content
            if "am" in content:
                index=content.index("am") #find the index of am
                time=content[index-1] #time is present is the previous index of am
            else:
                index=content.index("pm")
                time=content[index-1]
            print(time)
            emoji = '\N{THUMBS UP SIGN}'
            # or '\U0001f44d' or '👍'
            await message.add_reaction(emoji)

# When a member leaves the guild his data is deleted from the database
@client.event
async def on_member_remove(member):
    collection.find_one_and_delete({"user_id": member.id, "guild_id":member.guild.id})#delete the data from database from someone leaves the server

@client.event
async def on_reaction_add(reaction, user):
    content = reaction.message.content.lower() #obtain the content of message sent in channel
    content=re.sub('[^A-Za-z0-9: ]+', '', content) #remove special characters
    content = re.findall(r"[^\W\d_]+|\d+(?::\d+)?", content) #separate the string at spaces and numbers
    if any(item in ["am","pm"] for item in content): #if am or pm is found in the content
        if "am" in content:
            index=content.index("am") #find the index of am
            time=content[index-1] #time is present is the previous index of am
            period="am"
        else:
            index=content.index("pm")
            time=content[index-1]
            period="pm"
        try:
            user_reacted= collection.find_one({"user_id":user.id,"guild_id":reaction.message.guild.id}) 
            tz_reacted= user_reacted.get("timezone")   
            user_sent= collection.find_one({"user_id":reaction.message.author.id,"guild_id":reaction.message.guild.id}) 
            tz_sent= user_sent.get("timezone")  
            print("tz of user who reacted",tz_reacted) 
            print("tz of user who sent the message",tz_sent) 
            print("here workes the converter")
            convertTime(time,tz_sent,tz_reacted,period)
        except:
            pass
        
        try:
           await user.send("Hey")
        except:
            pass   

client.run(TOKEN)




