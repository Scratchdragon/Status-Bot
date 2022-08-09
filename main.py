import discord
import random
from discord.ext import tasks

client = discord.Client()

adverb = []
f = open("words/adverb.txt", "r")
adverb = f.read().split("\n")
f.close()

verb = []
f = open("words/verb.txt", "r")
verb = f.read().split("\n")
f.close()

adjective = []
f = open("words/adjective.txt", "r")
adjective = f.read().split("\n")
f.close()

noun = []
f = open("words/noun.txt", "r")
noun = f.read().split("\n")
f.close()

verb2 = ["being","becoming","pretend to be","acting","not being"]

def get_noun() :
	ret = random.choice(tuple(noun)) + " "
	if(random.randrange(0,2)==0):
		ret = random.choice(tuple(adjective)) + " " + ret
	return ret

def get_verb() :
	ret = random.choice(tuple(verb)) + " "
	if(random.randrange(0,2)==0):
		ret = random.choice(tuple(adverb)) + " " + ret
	return ret

def get_random_stat(type) :
	if(type==5):
		if(random.randrange(0,2)==0):
			return "a " + get_noun() + "competition"
		else:
			return "a " + get_verb().split(" ")[0] + "tournament"
	if(random.randrange(0,2)==0):
		nouna = get_noun()
		nounb = get_noun()
		if(nouna==nounb):
			nounb = "other " + nounb
		stat = nouna + get_verb() + nounb
	else:
		stat = get_noun() + random.choice(tuple(verb2)) + " " + random.choice(tuple(adjective))
	return stat
	
@client.event
async def on_ready():
	random.seed()
	print('Logged in as {0.user}'.format(client))
	loop.start()

@tasks.loop(seconds=30)
async def loop():
	types=["Listening to","Watching","Streaming","Competing in"]
	type=random.randrange(2,5)
	if(type==4):
		type = type + 1
	status=get_random_stat(type)
	await client.change_presence(activity=discord.Activity(name=status, type=type))
	print("Changed status to '" + types[type-2] + " " + status + "'")

@client.event
async def on_message(message):
	#adverb
	if message.content.startswith("~> adv"):
		f = open("words/adverb.txt","a")
		f.write("\n"+message.content[len("~> adv "):len(message.content)])
		print("Adding adverb " + message.content[len("~> adv "):len(message.content)])
		await message.channel.send("**[SB]:** Adding adverb " + message.content[len("~> adv "):len(message.content)])
		f.close()
	#adjective
	if message.content.startswith("~> adj"):
		f = open("words/adjective.txt","a")
		f.write("\n"+message.content[len("~> adj "):len(message.content)])
		print("Adding adjective " + message.content[len("~> adj "):len(message.content)])
		await message.channel.send("**[SB]:** Adding adjective " + message.content[len("~> adj "):len(message.content)])
		f.close()
	#noun
	if message.content.startswith("~> noun"):
		f = open("words/noun.txt","a")
		f.write("\n"+message.content[len("~> noun "):len(message.content)])
		print("Adding noun " + message.content[len("~> noun "):len(message.content)])
		await message.channel.send("**[SB]:** Adding noun " + message.content[len("~> noun "):len(message.content)])
		f.close()
	#verb
	if message.content.startswith("~> verb"):
		f = open("words/verb.txt","a")
		f.write("\n"+message.content[len("~> verb "):len(message.content)])
		print("Adding verb " + message.content[len("~> verb "):len(message.content)])
		await message.channel.send("**[SB]:** Adding verb " + message.content[len("~> verb "):len(message.content)])
		f.close()

	if message.content == "~R":
		print("Reload from app")
		await message.channel.send("**[SB]:** Reloading words")
		f = open("words/adverb.txt", "r")
		global adverb
		global verb
		global adjective
		global noun
		adverb = f.read().split("\n")
		f.close()
		f = open("words/verb.txt", "r")
		verb = f.read().split("\n")
		f.close()
		f = open("words/adjective.txt", "r")
		adjective = f.read().split("\n")
		f.close()
		f = open("words/noun.txt", "r")
		noun = f.read().split("\n")
		f.close()

	if message.content == "~X":
		print("Shutdown in app")
		await message.channel.send("**[SB]:** Shut down status bot")
		await client.logout()
		exit()

	if message.content.startswith("~< "):
		if message.content.endswith("adj"):
			await message.channel.send("\n".join(adjective))
		if message.content.endswith("adv"):
			await message.channel.send("\n".join(adverb))
		if message.content.endswith("verb"):
			await message.channel.send("\n".join(verb))
		if message.content.endswith("noun"):
			await message.channel.send("\n".join(noun))

try:
	f = open("token.txt","r")
	client.run(f.read(),bot=False)
	f.close()
except discord.HTTPException as e:
	if e.status == 429:
		print("The Discord servers denied the connection for making too many requests")
		print("Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests")
	else:
		raise e