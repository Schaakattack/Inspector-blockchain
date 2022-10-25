# app.py
'''
	A list of TODOs for our project

	TODO create database of wallets based on transactions in the blockchain
		TODO create a 'wallets' sqlite database
		TODO create a 'wallet' db with appropriate columns for data



'''

import sqlite3
con = sqlite3.connect('./db/wallet.db')
cur = con.cursor()

# ContractID		1
# BlockNumber		15783582
# TrxHash			0x16b2f0626d78ce1e95a6809d9582564366509b6bcea09ffd024fc556b1f9f00a
# Sender			0xf0e3ea754d038b979cd0124e2f1a4bf44f32746a
# Receiver,			0x87712434faa72a4cfdd9c22a486e38b43f3910e9
# TrxTimestamp,		2022-10-19 10:15:47
# Tokens			6000000

# TODO create SQL transaction to create transactions table
sql_create_transactions_db = '''
CREATE TABLE IF NOT EXISTS transactions(
	contract_id INT,
	
)
'''
# TODO execute the SQL transaction above
# # TODO import all data from WalletMapping.csv to the transactions table

# TODO create SQL transaction to create wallets table
sql_create_wallet_db = '''
CREATE TABLE IF NOT EXISTS wallets(
	wallet TEXT,
	tokenid INT,
	tokens REAL,
	last_tx TEXT
)
'''
# TODO execute the SQL transaction above
cur.execute(sql_create_wallet_db)
# TODO sort transaction table by transaction date
# TODO populate wallets table with all wallets (ie senders and receivers) from the transaction table
# TODO calculate wallet token totals based on the transactions in transaction table
# TODO create wallet token total "snapshots" every day 
#		... we could probably do this by creating a new 'wallets' table for each day from when
#		all transactions start (ie. do we need to know when the token was created / ICO'd?)

