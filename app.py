# app.py

# ==================================================================================================
# LIST OF ALL TODO's
# ==================================================================================================
'''
	A list of TODOs for our project
	basically taking Joe's Csv and create a visual for it.

	DONE create SQL transaction to create transactions table -- Chandler verify this is correct
	DONE create SQL transaction to create wallets table
	DONE import all data from WalletMapping.csv to the transactions table
	DONE populate wallets table with all unique wallets (senders and receivers) from the transactions table
	DONE write SQL to get all transactions sorted by transaction date

	chandler TODO chandler, can you take a stab and identifying all other TODOs in this project?

	TODO calculate wallet token totals based on the transactions in transaction table
	TODO create wallet token total "snapshots" every day 
		... we could probably do this by creating a new 'wallets' table for each day from when
		all transactions start (ie. do we need to know when the token was created / ICO'd?)
	TODO read in netowrkx and group accounts? barrabista?
	TODO corrolate wallets 
	TODO identify tool to plot data? matplotlib?

'''




# ==================================================================================================
# IMPORT STATEMENTS
# ==================================================================================================
import networkx as nx
from pathlib import Path
import pandas as pd
import sqlite3




# ==================================================================================================
# 'GLOBAL' VARIABLES WE WANT TO TRACK
# ==================================================================================================

ZERO_ADDRESS =	'0x0000000000000000000000000000000000000000'
DB_CONN = sqlite3.connect('./db/inspector.db')
DB_CURS = DB_CONN.cursor()




# ==================================================================================================
# CODE
# ==================================================================================================




# --------------------------------------------------------------------------------------------------
# connecting to our sqlite database


# --------------------------------------------------------------------------------------------------
# create all database tables if they don't already exist

# SQL statement to create transactions table
sql_create_transactions_table = '''
CREATE TABLE IF NOT EXISTS transactions(
	contract_id INT,
	block_num INT,
	tx_hash TEXT,
	sender TEXT,
	receiver TEXT,
	tx_timestamp TEXT,
	tokens REAL
)
'''
DB_CURS.execute(sql_create_transactions_table)

# SQL statement to create wallets table
sql_create_wallet_table = '''
CREATE TABLE IF NOT EXISTS wallets(
	wallet TEXT,
	tokenid INT,
	tokens REAL,
	last_tx TEXT
)
'''
DB_CURS.execute(sql_create_wallet_table)

# --------------------------------------------------------------------------------------------------
# reading the raw transactions and saving them to the database

# setting the raw transaction filepath for later use
raw_tx_filepath = Path('./data/walletmapping.csv')
# import all data from WalletMapping.csv to the transactions table
raw_tx_header = ["contract_id" , "block_num", "tx_hash", "sender", "receiver", "tx_timestamp", "tokens"]

# reading the raw transaction data from CSV into a dataframe for easy manipulation
raw_tx_transactions_df = pd.read_csv(
	filepath_or_buffer =	raw_tx_filepath,
	header =	0,
	names  =	raw_tx_header
)
print(raw_tx_transactions_df)

# writing the transactions to the database
# this currently REPLACES all transactions in the 'transactions' table
# TODO might want to wrap with try-catch block to allow a swap of if_exists='fail'
raw_tx_transactions_df.to_sql(
	name =	"transactions",
	con = 	DB_CONN,
	if_exists="replace",
	index=False 
)

# --------------------------------------------------------------------------------------------------
# code for populating the wallets table with all wallet addresses (senders and receivers) from the transaction table
#		read the sorted transactions table
#		join sender and receiver columns keeping only unique values
#		store unique values in the wallets table 'wallet' column
sql_populate_wallel_column_in_wallets_table = '''
INSERT OR IGNORE INTO wallets (wallet)
SELECT sender AS wallet FROM transactions 
UNION SELECT receiver FROM transactions
'''
# not actually executing this sql code because we're already done it once

# --------------------------------------------------------------------------------------------------
# build a dataframe of all transactions sorted by transaction date

# SQL code to get list of transactions by transaction date
sql_select_sort_tx_by_date = '''
SELECT
	tx_timestamp,
	sender,
	receiver,
	tokens
FROM transactions
ORDER BY tx_timestamp ASC
'''
# df index
sorted_tx_index = 'tx_timestamp'
# df columns
sorted_tx_cols  = ['sender', 'receiver', 'tokens']
# load sorted transactions into pandas dataframe
sorted_tx_df = pd.read_sql(
	sql =	sql_select_sort_tx_by_date, 
	con =	DB_CONN,
	parse_dates =	True,
	index_col =	sorted_tx_index,
	columns   =	sorted_tx_cols
)
print (sorted_tx_df)

# --------------------------------------------------------------------------------------------------
# calculate wallet token totals based on the transactions in transaction table

# TODO add code to be able to time slice transactions on a day-by-day basis
# current_day = None
# prior_day = None
for row in sorted_tx_df.iterrows():

	# current_time = row[0]
	# if current_time > current_day:
	# 	...
	
	print('--------------------------------')
	print('row index', row[0])

	print('----')
	print('sender', row[1].sender)
	
	# if not ZERO ADDRESS then subtract tokens from the sender wallet
	if not row[1].sender == ZERO_ADDRESS:

		# get sender wallet tokens
		sql_get_sender_wallet_tokens = "SELECT tokens FROM wallets WHERE wallet IS '" + row[1].sender + "'"
		DB_CURS.execute(sql_get_sender_wallet_tokens)
		sender_tokens = DB_CURS.fetchone()[0]
		print('sender wallet tokens', sender_tokens)

		# asserting because if sender_tokens are Null we've got a problem
		# assert(not sender_tokens == None)
		if sender_tokens == None:
			sender_tokens = 0
			print('sender wallet tokens None -> 0')
			print('sender wallet tokens', receiver_tokens)

		# removing tokens from sender wallet
		sender_tokens -= row[1].tokens
		print('sender wallet tokens', sender_tokens)
	else:
		print('ZERO ADDRESS - skipping subtraction')

	print('----')
	print('receiver', row[1].receiver)
	
	# getting receiver wallet tokens
	sql_get_receiver_wallet_tokens = "SELECT tokens FROM wallets WHERE wallet IS '" + row[1].receiver + "'"
	DB_CURS.execute(sql_get_receiver_wallet_tokens)
	receiver_tokens = DB_CURS.fetchone()[0]
	print('receiver wallet tokens', receiver_tokens)

	if receiver_tokens == None:
		receiver_tokens = 0
		print('receiver wallet tokens None -> 0')
		print('receiver wallet tokens', receiver_tokens)
	
	# adding tokens to receiver wallet
	receiver_tokens += row[1].tokens
	print('receiver wallet tokens', receiver_tokens)
	print('----')

	# recording sender & receiver token transactions in database
	if not row[1].sender == ZERO_ADDRESS:
		sql_update_sender_wallet_tokens = "UPDATE OR FAIL wallets SET tokens=? WHERE wallet=?"
		DB_CURS.execute(sql_update_sender_wallet_tokens, (sender_tokens, row[1].sender))
	
	sql_update_receiver_wallet_tokens = "UPDATE OR FAIL wallets SET tokens=? WHERE wallet=?"
	DB_CURS.execute(sql_update_receiver_wallet_tokens, (receiver_tokens, row[1].receiver))
	DB_CONN.commit()






# TODO create wallet token total "snapshots" every day 
# 	... we could probably do this by creating a new 'wallets' table for each day from when
# 	all transactions start (ie. do we need to know when the token was created / ICO'd?)
# TODO read in netowrkx and group accounts? barrabista?
"""
SELECT sender,
       receiver,
       SUM(tokens) AS tokens,
       COUNT(sender) AS num_of_transactions
FROM transactions
GROUP BY sender, receiver;
"""

node_sql = """
SELECT DISTINCT wallet
FROM wallets"""

edges_sql = """SELECT sender,
receiver,
SUM(tokens) AS tokens,
COUNT(sender) AS num_of_transactions
FROM transactions
GROUP BY sender, receiver"""

edges = pd.read_sql(edges_sql, con=DB_CONN)
nodes = pd.read_sql(node_sql, con=DB_CONN)

nodes_list = list(nodes['wallet'])

edges_sender = list(edges['sender'])
edges_receiver = list(edges['receiver'])
edges_zipped = list(zip(edges_sender, edges_receiver))

G = nx.Graph()
G.add_nodes_from(nodes_list)
G.add_edges_from(edges_zipped)

nx.draw(G)

# TODO check graph attempt and advise
# TODO identify tool to plot data? matplotlib?
