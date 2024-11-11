import discord
from discord.ext import commands
import re
import requests
import json
import math

bot = commands.Bot(command_prefix='>', self_bot=True)

#Replace this with your discord user id. its used to ping you when buy/sell transactions happen
USER_ID = 99999999999

#Define your discord channels here. These are channel IDs, enable discord developer settings and then right click the channel you want to watch and click Copy Channel ID
#just list however many you want
c1 = 29384902840923840
#c2 = 29859048309583905

#Discord Webhook for buy/sell notifications
DISCORD_WEBHOOK_URL = 'REPLACE ME WITH YOUR WEBHOOK'

#This is where you set your buy amounts for the channels. Values are listed in lamports. 
#1 sol = 1000000000 lamports
#you need 1 entry for each channel you have listed above

# example for 1 channel: 
# channels = {'29384902840923840':{'buy_amt':1000000000}}

#example for 2 channels: 
#channels = {'29384902840923840':{'buy_amt':1000000000}, '111119843220394':{'buy_amt':5000000000}}

channels = {'REPLACE ME WITH YOUR CHANNEL ID':{'buy_amt':1000000000}}



#RPC endpoint
API_URL = 'REPLACE ME WITH YOUR HELIUS RPC'

#Wallet address. NOT privkey
WALLET = 'REPLACE ME WITH YOUR WALLET ADDRESS'


def get_spl_token_balance(wallet_address, token_mint):
    headers = {
        'Content-Type': 'application/json'
    }

    # Helius specific RPC request payload
    data = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTokenAccountsByOwner",
        "params": [
            wallet_address,
            {
                "mint": token_mint
            },
            {
                "encoding": "jsonParsed"
            }
        ]
    }

    # Send request to Helius API
    response = requests.post(API_URL, json=data, headers=headers)
    print(response.text)
    result = response.json()
    print(result)
    # Process and return the balance
    if 'result' in result and result['result']['value']:
        token_account_info = result['result']['value'][0]['account']['data']['parsed']['info']
        balance = token_account_info['tokenAmount']['uiAmount']
        print(balance)
        return balance
    else:
        return 0

def send_discord_notification(subject, body):
    data = {
        "content": f"<@{USER_ID}> {subject}\n{body}"
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print("Notification sent successfully.")
    else:
        print(f"Failed to send notification. Status code: {response.status_code}")

def ape(ca, amt):
    return requests.get(f"http://localhost:3000/swap?coin={ca}&amt={amt}&slippage=300").text

def is_spl(message):
    spl_token_regex = r'[1-9A-HJ-NP-Za-km-z]{32,44}'    
    match = re.search(spl_token_regex, message)
    if match:
        return True, match.group(0)
    else:
        return False, None

def get_ca(pair):
    url = f'https://api.dexscreener.com/latest/dex/pairs/solana/{pair}'
    ca = json.loads(requests.get(url).text)['pairs'][0]['baseToken']['address']
    return ca

def sell(ca, amt):
    print(f"http://localhost:3000/sell?coin={ca}&amt={amt}&slippage=300")
    return requests.get(f"http://localhost:3000/sell?coin={ca}&amt={amt}&slippage=300").text

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.event
async def on_message(message):
    buy_amt = 250000000
    if message.channel.id == c1: #or message.channel.id == c2 or message.channel.id == c3 or message.channel.id == c4:
        print(f"Message from {message.author}: {message.content}")
        #ignore posts from Rick bot
        if "rick" in str(message.author).lower():
            return
        isSPL, addy = is_spl(message.content)
        if isSPL:
            if 'https://dexscreener.com/solana/' in message.content:
                addy = get_ca(addy)
            print(f'Token Address Found: {addy}')
            buy_amt = channels[str(message.channel.id)]['buy_amt']
            print(f"Buying {buy_amt} lamports of {addy}")
            x = ape(addy, buy_amt)
            print(f"Response: {x}")
            if "amount" in x:
                send_discord_notification(addy, json.loads(x)['message'].split(': ')[1])
        

    await bot.process_commands(message)
bot.run('REPLACE ME WITH YOUR DISCORD TOKEN')