# Discord Solana Token Buyer Bot

This Discord bot listens to specific Discord channels and automatically buys Solana tokens (SPL tokens) whenever they are posted in those channels.

## Features

- Listens for messages containing Solana (SPL) token addresses in designated Discord channels.
- Automatically buys the specified amount of tokens (in lamports) whenever a valid token address is posted.
- Sends notifications to Discord about buy/sell transactions.
- Works with custom channels and adjustable buy amounts.

## Requirements

- Python 3.7 or higher
- `discord.py-self` library
- `requests` library
- A running local instance of my SPL token swap API posted on my github
- Helius RPC credentials

## Installation

1. Clone the repository:
   - `git clone https://github.com/yourusername/discord-solana-token-buyer.git`
   - `cd discord-solana-token-buyer`

2. Install Discord Py-Self
   - `py -m pip install -U discord.py-self`
     
3. Install Requests
   `py -m pip install requests`

## Setup

1. Edit the python file and enter all information required
     - your discord oauth token
     - your wallet public address
     - your discord user id
     - discord channels to watch
     - discord buy amounts for those channels
