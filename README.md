# Network Monitor

This project is a distributed network monitoring system that utilizes persistent TCP connections. 

A central console client connects to and communicates with one or more designated remote servers.
The remote servers, which are always online, receive commands from the central console to start or stop monitoring specific connections.
Each monitored connection reports relevant data back to the central console for display. 

Both the central console and remote servers are coded in Python primarily using sockets. 

For a brief video demo, see this link: https://youtu.be/uYxvBm_T_9A 

## Detailed Specs

Central Console Functionality: 
* A basic command prompt interface is present for users to easily access its functionality
* Can connect to one or more remote monitoring servers, each identified by its respective IP and port number, via persistent TCP
* Each remote server connection is run on a separate daemon thread to allow for multitasking 
* Users can configure a connection to monitor through the command prompt via a step-by-step flow (with support for HTTP, HTTPS, ICMP, DNS, NTP, TCP, and UPD connections)
* All connection monitoring configurations are saved and can be easily accessed again later (through a saved file in the same directory)
* Users can command each remote server to start or stop an active connection monitoring task
* The console displays monitoring data sent by each remote server in real-time

Remote Server Functionality:
* Configurable IP and port number
* Accept persistent TCP connections from the central console client
* Monitor one or more HTTP, HTTPS, ICMP, DNS, NTP, TCP, and UDP connections based on the configuration sent by the central console
* Each monitoring task is assigned to a daemon thread to allow multitasking
* Send monitoring data back to the console client for display, with the unique identifier for each remote server 
* Receive and execute commands from the central console to stop an active monitoring task

## Program Setup
1. See the requirements.txt file for all possible dependencies and make sure they are installed, including Python 3 or newer
2. Download the mon_server.py and mysocket.py files and save them to a directory
3. Open mon_server.py and set the server_address (IP) and server_port (port number) variables as desired (by default they are 127.0.0.1 and 65240)
   * Each mon_server represents an individual remote server instance, feel free to run as many as desired as long as they use distinct IP/port combinations and file names
4. Run a separate instance of mon_server.py for each desired remote server in an IDE such as Pycharm to start that remote server
5. Then open mysocket.py DIRECTLY, outside of an IDE (this is required due to the presence of the prompt toolkit package)
6. Follow the on-screen directions to use the program, you can also refer to the video demo above for more help
7. If you run into issues, please ensure that the remote server instances are running before you try to access them via the console
