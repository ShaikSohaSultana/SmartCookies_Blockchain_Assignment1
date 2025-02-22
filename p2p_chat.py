import socket
import threading
import select

class Peer:
    def __init__(self, name, port):
        self.name = name
        self.port = port
        self.peers = set()  # Active peers
        self.all_peers = set()  # All peers who have interacted
        self.server_socket = None
        self.running = True

    def start_server(self):
        """Starts the server to listen for incoming connections."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server_socket.bind(("0.0.0.0", self.port))
            self.server_socket.listen(5)
            host_ip = socket.gethostbyname(socket.gethostname())
            print(f"[SERVER] Listening on {host_ip}:{self.port}")
        except Exception as e:
            print(f"[ERROR] Failed to start server: {e}")
            return

        while self.running:
            try:
                readable, _, _ = select.select([self.server_socket], [], [], 1)
                if readable:
                    client_socket, addr = self.server_socket.accept()
                    threading.Thread(target=self.handle_client, args=(client_socket, addr), daemon=True).start()
            except OSError:
                if not self.running:
                    print("[SERVER] Server shutting down.")
                    break

    def handle_client(self, client_socket, addr):
        """Handles messages received from connected peers."""
        try:
            message = client_socket.recv(1024).decode("utf-8").strip()
            if not message:
                return

            # Handle connection requests
            if "CONNECT_REQUEST" in message:
                peer = message.split()[0]
                print(f"Connection request received from {peer}. Do you accept? (y/n): ", end="")
                choice = input().strip().lower()
                if choice == 'y':
                    client_socket.send("CONNECTED".encode())
                    self.peers.add(peer)
                    self.all_peers.add(peer)
                    print(f"Connected to {peer}.")
                else:
                    client_socket.send("REJECTED".encode())
                    print(f"Connection request from {peer} rejected.")
                client_socket.close()
                return

            # Handle normal messages
            parts = message.split(" ", 2)
            if len(parts) == 3:
                sender_ip_port, team_name, chat_message = parts
                sender_ip, sender_port = sender_ip_port.split(":")
                sender_port = int(sender_port)
                
                # Print the received message in the desired format
                print(f"{sender_ip}:{sender_port} [{team_name}]: {chat_message}")
                self.add_peer(sender_ip, sender_port)
                
                if chat_message.lower() == "exit":
                    print(f"[INFO] Peer {sender_ip}:{sender_port} disconnected.")
                    self.peers.discard((sender_ip, sender_port))
            else:
                print(f"[RECEIVED] Invalid format from {addr}: {message}")

            client_socket.sendall(f"[ACK] Message received from {self.port}".encode("utf-8"))
        except Exception as e:
            print(f"[ERROR] Handling client {addr}: {e}")
        finally:
            client_socket.close()

    def send_message(self, ip, port, message):
        """Sends a message to a peer."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.settimeout(5)
                client_socket.connect((ip, port))
                sender_ip = socket.gethostbyname(socket.gethostname())
                formatted_message = f"{sender_ip}:{self.port} {self.name} {message}"
                client_socket.sendall(formatted_message.encode("utf-8"))
                print(f"[SENT] {formatted_message}")

                response = client_socket.recv(1024).decode("utf-8").strip()
                print(response)
                
                self.add_peer(ip, port)  
        except (socket.timeout, ConnectionRefusedError):
            print(f"[ERROR] Peer {ip}:{port} is unreachable. Removing from list.")
            self.peers.discard((ip, port)) 
        except Exception as e:
            print(f"[ERROR] Sending message to {ip}:{port}: {e}")

    def add_peer(self, ip, port):
        """Adds a peer to the list if not already present."""
        peer = f"{ip}:{port}"
        if peer not in self.peers:
            self.peers.add(peer)
            self.all_peers.add(peer)
            print(f"[PEER] Added {peer} to the list.")

    def query_peers(self):
        """Displays active and all peers."""
        if self.peers:
            print("\nActive Peers:")
            for peer in self.peers:
                print(peer)
        else:
            print("No active peers.")

        if self.all_peers:
            print("\nAll Peers (who have interacted with this system):")
            for peer in self.all_peers:
                print(peer)
        else:
            print("No peers have interacted yet.")

    def send_connection_request(self, ip, port):
        """Sends a connection request to a peer."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((ip, port))
                sender_ip = socket.gethostbyname(socket.gethostname())
                connect_message = f"{sender_ip}:{self.port} CONNECT_REQUEST"
                client_socket.sendall(connect_message.encode("utf-8"))
                
                response = client_socket.recv(1024).decode("utf-8").strip()
                if response == "CONNECTED":
                    self.peers.add(f"{ip}:{port}")
                    self.all_peers.add(f"{ip}:{port}")
                    print(f"Successfully connected to {ip}:{port}")
                elif response == "REJECTED":
                    print(f"Connection request to {ip}:{port} was rejected.")
                
                client_socket.close()
        except ConnectionRefusedError:
            print(f"[ERROR] Connection refused by {ip}:{port}. Ensure the peer is running.")
        except Exception as e:
            print(f"[ERROR] Connecting to {ip}:{port}: {e}")

    def disconnect_from_peers(self, peer_to_disconnect=None):
        """Disconnects from all active peers or a specified peer."""
        if peer_to_disconnect:
            try:
                ip, port = peer_to_disconnect.split(":")
                port = int(port)
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                    client_socket.connect((ip, port))
                    client_socket.send(f"{socket.gethostbyname(socket.gethostname())}:{self.port} DISCONNECTED".encode())
                    client_socket.close()
                self.peers.discard(peer_to_disconnect)
                print(f"Disconnected from {peer_to_disconnect}")
            except Exception as e:
                print(f"Error disconnecting from {peer_to_disconnect}: {e}")
        else:
            for peer in list(self.peers):
                try:
                    ip, port = peer.split(":")
                    port = int(port)
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                        client_socket.connect((ip, port))
                        client_socket.send(f"{socket.gethostbyname(socket.gethostname())}:{self.port} DISCONNECTED".encode())
                        client_socket.close()
                    self.peers.discard(peer)
                    print(f"Disconnected from {peer}")
                except Exception as e:
                    print(f"Error disconnecting from {peer}: {e}")

    def connect_to_active_peers(self):
        """Tries to connect to all active peers."""
        if not self.peers:
            print("[INFO] No active peers to connect to.")
            return

        for peer in list(self.peers):
            try:
                ip, port = peer.split(":")
                port = int(port)
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                    client_socket.connect((ip, port))
                    sender_ip = socket.gethostbyname(socket.gethostname())
                    connect_message = f"{sender_ip}:{self.port} CONNECT_REQUEST"
                    client_socket.sendall(connect_message.encode("utf-8"))
                    
                    response = client_socket.recv(1024).decode("utf-8").strip()
                    if response == "CONNECTED":
                        print(f"[SUCCESS] Connected to {ip}:{port}")
                    elif response == "REJECTED":
                        print(f"[REJECTED] Connection request to {ip}:{port} was denied.")
                    
                    client_socket.close()
            except ConnectionRefusedError:
                print(f"[ERROR] Connection refused by {peer}. Removing from active list.")
                self.peers.discard(peer)
            except Exception as e:
                print(f"[ERROR] Connecting to {peer}: {e}")

    def stop(self):
        """Stops the server and closes the socket."""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
            print("[SERVER] Server socket closed.")

def main():
    """Main menu for peer-to-peer messaging."""
    name = input("Enter your team name: ")
    port = int(input("Enter your port number: "))
    peer = Peer(name, port)
    
    # Start the server and ensure it binds before showing the menu
    server_thread = threading.Thread(target=peer.start_server, daemon=True)
    server_thread.start()
    
    # Small delay to allow the server to start and print its message
    import time
    time.sleep(1)

    while True:
        print("\n***** Menu *****")
        print("1. Send message")
        print("2. Query active peers")
        print("3. Send connection request")
        print("4. Disconnect from all peers")
        print("5. Disconnect from a specific peer")
        print("6. Connect to active peers")
        print("0. Quit")
        
        choice = input("Do you want to make a choice? (y/n): ").strip().lower()
        if choice == 'y':
            choice = input("Enter choice: ")
            
            if choice == "1":
                ip = input("Enter the recipient’s IP address: ")
                port = int(input("Enter the recipient’s port number: "))
                message = input("Enter your message: ")
                peer.send_message(ip, port, message)
            elif choice == "2":
                peer.query_peers()
            elif choice == "3":
                ip = input("Enter peer’s IP address: ")
                port = int(input("Enter peer’s port number: "))
                peer.send_connection_request(ip, port)
            elif choice == "4":
                peer.disconnect_from_peers()
            elif choice == "5":
                peer_to_disconnect = input("Enter the peer to disconnect (format: IP:Port): ")
                peer.disconnect_from_peers(peer_to_disconnect)
            elif choice == "6":  
                peer.connect_to_active_peers()
            elif choice == "0":
                peer.stop()
                print("Exiting...")
                break
            else:
                print("[ERROR] Invalid choice. Please try again.")
        elif choice == 'n':
            print("[INFO] Infinite loop mode enabled. Press Ctrl+C to stop.")
            while True:
                pass
        else:
            print("[ERROR] Invalid input. Please try again.")

if __name__ == "__main__":
    main()            