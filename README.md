# Peer-to-Peer Chat Application

## Team Information
- **Team Name**: Smart Cookies  
- **Team Members & Roll Numbers**:
  - Eedubilli Lathika Priya - 230001026  
  - Goskula Harshitha - 230001027  
  - Shaik Soha Sultana - 230001071  

## Overview
This Peer-to-Peer (P2P) Chat Application, implemented in Python, enables direct communication between multiple peers while maintaining a dynamic list of connected users.

## Features
1. **Simultaneous Send & Receive**: Multi-threaded for concurrent messaging.
2. **Peer List Management**: Dynamically updates active and all-time peer lists.
3. **Structured Message Format**: Ensures consistent communication.
4. **Query Functionality**: Allows users to view connected peers.
5. **Manual & Automatic Peer Connectivity**: Supports both manual connections and auto-connect features.
6. **Duplicate Entry Prevention**: Maintains unique peer entries.
7. **Ephemeral Port Handling**: Correctly manages changing port numbers.
8. **Disconnect Options**: Allows disconnecting from all or specific peers.
9. **Connection Request Handling**: Manages peer connection requests.

## System Requirements
- **Programming Language**: Python 3.x
- **Libraries**: socket, threading, select
- **Operating System**: Windows / Linux / macOS

## Installation & Setup
1. Clone the repository:
git clone https://github.com/yourusername/p2p-chat-app.git
cd p2p-chat-app

2. Run the application:
python p2p_chat.py

3. Enter your team name and listening port when prompted.

## Usage Instructions
### Menu Options
** Menu **

1.Send message

2.Query active peers

3.Send connection request

4.Disconnect from all peers

5.Disconnect from a specific peer

6.Connect to active peers

7.Quit


### Sending a Message
1. Choose option 1
2. Enter recipient's IP, port, and your message

### Querying Active Peers
Choose option 2 to view connected peers

### Connecting to Peers
- Option 3: Manually connect to a peer
- Option 6: Auto-connect to all known peers

### Disconnecting
- Option 4: Disconnect from all peers
- Option 5: Disconnect from a specific peer

### Exiting the Application
Choose option 0

## Message Format
Messages follow this structure:

<IP ADDRESS:PORT> <Team Name> <Your Message>


## Technical Implementation
- Multi-threading for concurrent operations
- TCP sockets for reliable communication
- Dynamic peer list management
- Handling of ephemeral ports

## Test Case: Basic Communication
1. Start two instances (Peer A and Peer B) on different terminals.
2. Peer A: TeamA, Port 5000
3. Peer B: TeamB, Port 6000
4. Peer A: Send connection request to Peer B
5. Peer B: Accept connection
6. Peer A: Send message "Hello from TeamA!"
7. Peer B: Should receive the message
8. Peer B: Query active peers (should show Peer A)

This test demonstrates basic connectivity, messaging, and peer list updating.

Current Date: Saturday, February 22, 2025, 10:18 PM IST
