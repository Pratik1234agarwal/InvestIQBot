# bot.py
import os
import random
import pickle

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')


users = {}
try:
    file = open('tasks', 'rb')
    users = pickle.load(file)
    file.close()
    print(users)
except:
    users = {}


@bot.command(name="view", help="View All the Tasks Added")
async def view_task(ctx):
    author_id = ctx.message.author.id
    message = []
    if not author_id in users.keys():
        users[author_id] = []
        await ctx.send("No Task has been added yet")
    else:
        if(len(users[author_id]) == 0):
            await ctx.send("No Task has been added yet")
        else:
            for index, task in enumerate(users[author_id]):
                message.append(f'{index + 1}. {task}\n')
            message.append("These are the tasks you added.")
            await ctx.send(''.join(message))


@bot.command(name="add", help="Add a Task. !add 'Task detail' ")
async def create_task(ctx, args):
    author_id = ctx.message.author.id
    if not author_id in users.keys():
        users[author_id] = []
    users[author_id].append(args)
    write_users()
    await ctx.send("Task Added\n !view to view all tasks")


@bot.command(name="mark", help="Mark a task as completed. !mark 1")
async def mark_complete(ctx, args=1):
    author_id = ctx.message.author.id
    if not author_id in users.keys():
        users[author_id] = []
    index = -1
    for i, value in enumerate(users[author_id]):
        if(i == args - 1):
            index = i
            users[author_id][index] = f'~~{value}~~'
    if index == -1:
        await ctx.send("Task Number Not found")
    else:
        write_users()
        await ctx.send("Task marked as complete")


@bot.command(name="clear", help="Clear All Task or a particular one\n !clear all\n!clear 1")
async def clear(ctx, args):
    author_id = ctx.message.author.id

    if(args == 'all'):
        users[author_id] = []
        await ctx.send("All task has been cleared")
    else:
        if not author_id in users.keys():
            users[author_id] = []
            await ctx.send("There are no task added")
        else:
            if int(args) > len(users[author_id]):
                await ctx.send("Invalid Task id entered")
            else:
                del users[author_id][int(args)-1]
                await ctx.send("Task Cleared\n!view to view all tasks")
    write_users()


@bot.event
async def on_command_error(ctx, error):
    print(ctx)
    print(ctx.message)
    if isinstance(error, commands.BadArgument):
        await ctx.send('I could not find that member...')
    else:
        await ctx.send("Invalid Command")


def write_users():
    try:
        file=open('tasks', 'wb')
        pickle.dump(users, file)
        file.close()
    except:
        print("Not able to save to file")


bot.run(TOKEN)
