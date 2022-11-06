# Inspector Blockchain

This project is a proposed solution for mapping blockchain wallets for a specific token contract in order to identify large wallet holders and eventually track when transactions are made to-from those wallets.

### Executive Summary

* Many token projects are enrichment schemes.
* As DeFi is mostly unregulated, founders can create large numbers of tokens and transfer them to insider wallets before a token project's Initial Coin Offering (ICO).
* Founders can then market and launch the token, creating instant value for themselves and other insiders. Retail investors often have no idea this occurs.
* This project aims to 'pierce the veil' and shed light on this activity.

### Project Goal

* Allow anyone to easily identify insider wallets and large money transactions in any token project.

### Project Approach

1. Crawl the Ethereum Blockchain
2. Record all transactions related to the token of interest
3. Identify all wallets sending or receiving that token
4. Graph the relationship between wallets sending and receiving the token
5. Highlight wallets of interest

### Project Evaluation & Analysis

* Each aspect (crawler, data base, visualization) works.
* NetworkX wasn't sufficient by itself, and the default graphing library (matplotlib) resulted in some pretty nasty graphs.
* We found that pyplot, and graphviz greatly improved the positional layout of the nodes. Plotly helps make things pretty to look at.
* Scaling and sizing will be an ongoing battle as different projects have different supply and incentive structures.

### Conclusions

* Inspector blockchain core concept is proven.
* Great start at displaying large wallets and displaying the connections between those.
* The visuals needs improvement.
* Works well to identify outliers.
* API calls will be a limiting factor as we’re limited to 5 calls / second.

### A Graph of Wallets with Tokens > 1M

<p align="center">
<img src="https://github.com/Schaakattack/Inspector-blockchain/blob/main/images/Screen%20Shot%202022-11-03%20at%203.32.52%20PM.png?raw=true" 
width="95%" />
</p>

### Next Steps

1. make blockchain crawler as efficient as possible and running 24/7.
2. would be a great improvement to identify insider wallets, liquidity pools, smart contracts during the crawl.
3. develop a decent graphical representation of insider wallets (founders, liquidity pools, etc.) vs retail owners.
4. setup a website to simplify inspection and notification.
5. increase capability to crawl more tokens.
6. add support for Solana.

---

# Technologies

The stable version of this project can be run on Windows, Mac OS, or Linux as long as the user's 
environment has the following:
- python 3.7
- jupyterlab
- networkx
- sqlite3
- plotly
- pydot
- graphviz

---

# Installation Guide

You have a few options to get this code on your computer, two popular options are:

1. Download a ZIP of this repositories files 
[here](https://github.com/Schaakattack/Inspector-blockchain/archive/refs/heads/main.zip).

2. [Fork this respository](https://docs.github.com/en/get-started/quickstart/fork-a-repo "Fork a Repo - 
GitHub Docs") to your github account.

<p align="center">
<img src="https://github.com/Warp-9000/uw-fintech-2022-module01-challenge/blob/main/instructions/github-fork-button-screenshot.png?raw=true" 
alt="Fork UI on GitHub.com"
width="55%"/>
</p>

After forking the respository you can use `git clone 
your-username@domain.com:your-git-username/Inspector-blockchain.git` 
to download a copy of the forked respository to your computer.

Forking has the added benefit of enabling your to easily keep your copy of the 
application up-to-date should any changes or improvements be made in the future.

---

# Usage

***Please note:*** these usage instructions assume you are running JupyterLab from the commandline.

After forking the code you can:

1. Load the `generate_data.ipynb` jupyter notebook and run all cells.
	- this will populate `inspector.db` and generate the data necessary to build a graph.
<br><br>

2. Load the `display_graph.ipynb` jupyter notebook and run all cells.
	- this will read `inspector.db` and build a node and edge list, create a graph, and display it with plotly.

---

# Contributors

This project was created by Chandler, Nathan, and Peter.

<a href="https://github.com/Schaakattack/Inspector-blockchain/graphs/contributors">
<img src="https://contrib.rocks/image?repo=schaakattack/inspector-blockchain" />
</a>
