import os
from datetime import datetime
import requests
import asyncio
import json
from dotenv import load_dotenv
import discord
from discord.commands import Option
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.blocking import BlockingScheduler


intents = discord.Intents.default()
intents.members = True
bot = discord.Bot(intents=intents)

async def fetch_contests(sched, bot: discord.Bot):
	API_URL = "https://codeforces.com/api/contest.list"
	data = requests.get(url=API_URL).json()
	for entry in data["result"]:
		if entry["phase"] == "BEFORE" and "startTimeSeconds" in entry.keys():
			start_time = int(entry["startTimeSeconds"])
			scheduled = []
			if not "Div. 1" in entry["name"] and not "Div. 2" in entry["name"] and not "Div. 3" in entry["name"] and not "Div. 4" in entry["name"]:
				entry["name"] += "Div. 1Div. 2Div. 3Div. 4"
			if "Div. 1" in entry["name"]:
				print("New Div 1 contest: " + entry["name"] + "id: " + str(entry["id"]))
				if os.path.isfile(f'{os.path.dirname(__file__)}\\subscription1.csv'):
					with open(f'{os.path.dirname(__file__)}\\subscription1.csv', 'r') as f:
						user_ids = list(map(int, f.read().split(',')[:-1]))
					for user_id in user_ids:
						if not user_id in scheduled:
							sched.add_job(notify_users, 'date', run_date=datetime.fromtimestamp(start_time - 60*60*24), args=[sched, bot, user_id, 1, entry["id"], start_time, "1d"])
							sched.add_job(notify_users, 'date', run_date=datetime.fromtimestamp(start_time - 60*60), args=[sched, bot, user_id, 1, entry["id"], start_time, "1h"])
							sched.add_job(notify_users, 'date', run_date=datetime.fromtimestamp(start_time - 60*10), args=[sched, bot, user_id, 1, entry["id"], start_time, "10m"])
							scheduled.append(user_id)
			if "Div. 2" in entry["name"]:
				print("New Div 2 contest: " + entry["name"] + "id: " + str(entry["id"]))
				if os.path.isfile(f'{os.path.dirname(__file__)}\\subscription2.csv'):
					with open(f'{os.path.dirname(__file__)}\\subscription2.csv', 'r') as f:
						user_ids = list(map(int, f.read().split(',')[:-1]))
					for user_id in user_ids:
						if not user_id in scheduled:
							sched.add_job(notify_users, 'date', run_date=datetime.fromtimestamp(start_time - 60*60*24), args=[sched, bot, user_id, 2, entry["id"], start_time, "1d"])
							sched.add_job(notify_users, 'date', run_date=datetime.fromtimestamp(start_time - 60*60), args=[sched, bot, user_id, 2, entry["id"], start_time, "1h"])
							sched.add_job(notify_users, 'date', run_date=datetime.fromtimestamp(start_time - 60*10), args=[sched, bot, user_id, 2, entry["id"], start_time, "10m"])
							scheduled.append(user_id)
			if "Div. 3" in entry["name"]:
				print("New Div 3 contest: " + entry["name"] + "id: " + str(entry["id"]))
				if os.path.isfile(f'{os.path.dirname(__file__)}\\subscription3.csv'):
					with open(f'{os.path.dirname(__file__)}\\subscription3.csv', 'r') as f:
						user_ids = list(map(int, f.read().split(',')[:-1]))
					for user_id in user_ids:
						if not user_id in scheduled:
							sched.add_job(notify_users, 'date', run_date=datetime.fromtimestamp(start_time - 60*60*24), args=[sched, bot, user_id, 3, entry["id"], start_time, "1d"])
							sched.add_job(notify_users, 'date', run_date=datetime.fromtimestamp(start_time - 60*60), args=[sched, bot, user_id, 3, entry["id"], start_time, "1h"])
							sched.add_job(notify_users, 'date', run_date=datetime.fromtimestamp(start_time - 60*10), args=[sched, bot, user_id, 3, entry["id"], start_time, "10m"])
							scheduled.append(user_id)
			if "Div. 4" in entry["name"]:
				print("New Div 4 contest: " + entry["name"] + "id: " + str(entry["id"]))
				if os.path.isfile(f'{os.path.dirname(__file__)}\\subscription4.csv'):
					with open(f'{os.path.dirname(__file__)}\\subscription4.csv', 'r') as f:
						user_ids = list(map(int, f.read().split(',')[:-1]))
					for user_id in user_ids:
						if not user_id in scheduled:
							sched.add_job(notify_users, 'date', run_date=datetime.fromtimestamp(start_time - 60*60*24), args=[sched, bot, user_id, 4, entry["id"], start_time, "1d"])
							sched.add_job(notify_users, 'date', run_date=datetime.fromtimestamp(start_time - 60*60), args=[sched, bot, user_id, 4, entry["id"], start_time, "1h"])
							sched.add_job(notify_users, 'date', run_date=datetime.fromtimestamp(start_time - 60*10), args=[sched, bot, user_id, 4, entry["id"], start_time, "10m"])
							scheduled.append(user_id)
			pass

async def notify_users(sched, bot: discord.Bot, user_id: discord.User.id, div, contest_id, start_time: int, time_in_advance):
	print(f'Notify {user_id} for contest {contest_id}')
	with open(f'{os.path.dirname(__file__)}\\dm_channels.json', 'r') as f:
		dm_channels = json.load(f)
	if not user_id in dm_channels.keys():
		user = bot.get_user(user_id)
		new_dm_channel = await asyncio.gather(bot.create_dm(user))
		dm_channels[str(user_id)] = str(new_dm_channel[0].id)
		with open(f'{os.path.dirname(__file__)}\\dm_channels.json', 'w') as f:
			f.write(json.dumps(dm_channels))
	if time_in_advance == "1d":
		await bot.get_channel(int(dm_channels[str(user_id)])).send(f'New Div. {div} contest in 1 day on {datetime.fromtimestamp(start_time)}\n'
															   +f'Regestrationlink: https://codeforces.com/contestRegistration/{contest_id}')
	elif time_in_advance == "1h":
		await bot.get_channel(int(dm_channels[str(user_id)])).send(f'Div. {div} contest in 1 hour\n'
																	 +f'Regestrationlink: https://codeforces.com/contestRegistration/{contest_id}')
	elif time_in_advance == "10m":
		await bot.fetch_channel(int(dm_channels[str(user_id)])).send(f'Div. {div} contest starts in 10 min. Last chance for registration:\n'
																	 +f'https://codeforces.com/contestRegistration/{contest_id}')

@bot.slash_command(name = "subscribe_cf", description = "Subscribe to the codeforces contest notifications")
async def subscribe_cf(ctx, div: Option(str, "Choose which div to subscribe to")):
	if div in "1234":
		with open(f'{os.path.dirname(__file__)}\\subscription{div}.csv', 'r+') as f:
			if not str(ctx.author.id) in f.read():
				f.write(f'{ctx.author.id},')
				await ctx.respond(f'You have been added to div {div}')
			else:
				await ctx.respond(f'You are already subscribed to div {div}')
	else:
		await ctx.respond("Only 1, 2, 3 and 4 are valid divs")

@bot.event
async def on_ready():
	print(f'Logged in as {bot.user}')
	sched = AsyncIOScheduler()
	sched.add_job(fetch_contests, args=[sched, bot])
	sched.start()

load_dotenv()
TOKEN = os.environ.get("TOKEN")

if TOKEN:
	bot.run(TOKEN)
	pass

if not TOKEN:
	print("No TOKEN or .env file found")
	pass