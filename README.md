# Peer-to-Peer Communication System

## Project Description
This project implements a **Peer-to-Peer (P2P) communication system** that allows multiple peers to connect, send messages, and manage connections. It is designed to facilitate decentralized communication between nodes in a network using Python's 'socket' and 'threading' libraries.

## Features
1. **Send Message**: Allows a peer to send a message to another peer by specifying their IP address and port number.

2. **Query Active Peers**: Displays the list of all currently known peers in the network.

3. **Connect to Active Peers**: Establishes connections with all known peers.

4. **Receive Messages**: Listens for incoming messages from other peers and updates the list of active peers.

5. **Disconnect Options**:

   -Disconnect from all peers.

   -Disconnect from a specific peer (future implementation scope).

7. **Quit**: Exits the application.

## How It Works
Each peer runs its own server to listen for incoming connections and messages.
Peers maintain a list of active connections ('peers') that is dynamically updated as messages are exchanged.
Messages include the sender's IP address and port, which are used to identify and add new peers.

## Installation and Setup

1. Clone this repository to your local machine.

2. Ensure Python 3.x is installed on your system.

3. Run the script using:
  ''' bash python p2p_chat.py'''

4. Follow the prompts to:

   -Enter your team name.

   -Specify your port number for hosting the server.

## Usage Instructions
1. After starting the program, you will see a menu with options:
    -Select "1" to send a message by specifying the recipient's IP, port, and message content.
   
    -Select "2" to view all active peers in the network.
   
    -Select "3" to connect to all known peers.
   
    -Select "0" to quit the application.
   
3. The program runs continuously until you choose to exit.

## Code Overview
The main functionalities are implemented as follows:
  
  -receive_messages: Handles incoming messages and updates the peer list dynamically.
  
  -send_message: Sends messages formatted with sender details and team name.
  
  -query_peers: Displays all connected peers.
  
  -connect_to_peers: Attempts connections with all known peers.

## Group Information
Group Name: Smart Cookies

Group Members:
  
  -Eedubilli Lathika Priya (Roll No: 230001026)
  
  -Goskula Harshitha (Roll No: 230001027)
  
  -Shaik Soha Sultana (Roll No: 230001071)
