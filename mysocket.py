import socket
import threading
import random
import uuid
import prompt_toolkit
from prompt_toolkit import prompt
import pickle

# server_address = '127.0.0.1'
# server_port = 51426


def monitor_hub():

    monitor_dict = {}
    monitor_dict[1] = {"uid": ("MON_SERV_" + '1'), "ip": '127.0.0.1', "port": 51426}
    monitor_dict[2] = {"uid": ("MON_SERV_" + '2'), "ip": '127.0.0.1', "port": 65240}
    job_dict = {}
    serv_dict = {}
    ser_num = 1
    monitor_num = 3
    job_num = 1
    print_lock = threading.Lock()

    print_lock.acquire()
    print("Welcome to the monitor hub service!\n")
    print_lock.release()

    stop_flag = False
    while stop_flag == False:
        if len(monitor_dict) == 0:

            print_lock.acquire()
            print("Begin by connecting to a remote monitoring server.")
            print_lock.release()

            monitor_num = add_monitor(monitor_dict, monitor_num, print_lock)

        print_lock.acquire()
        print("\nChoose a command to execute:")
        print("1. Reconnect dropped monitor service\n" + "2. Rerun saved monitor service\n" + "3. Run new monitor service\n"
              + "4. Stop active monitor service\n" + "5. Add new monitor server\n" + "6. Exit program\n")
        print_lock.release()

        while True:
            menu_select = prompt("Enter the integer next to the command to continue: ")
            if menu_select not in ['1', '2', '3', '4', '5', '6']:

                print_lock.acquire()
                print("\nCommand not recognized, try again!")
                print_lock.release()

                continue
            else:
                break

        menu_select = int(menu_select)

        match menu_select:
            case 1:
                print("tbd")

            case 2:
                if len(serv_dict) == 0:
                    try:
                        file = open("saved_config", "rb")

                    except:

                        print_lock.acquire()
                        print("No saved monitor services available")
                        print_lock.release()

                    else:
                        serv_dict = pickle.load(file)
                        ser_num = len(serv_dict) + 1
                        file.close()

                serv_number = pick_service(serv_dict, print_lock, ser_num)
                serv_entry = serv_dict[serv_number]
                job_num = add_job(serv_entry, monitor_dict, monitor_num, job_dict, job_num, print_lock)

            case 3:
                ser_act, ser_num = serv_add(serv_dict, ser_num, print_lock)
                job_num = add_job(ser_act, monitor_dict, monitor_num, job_dict, job_num, print_lock)
                file = open("saved_config", "wb")
                pickle.dump(serv_dict, file)
                file.close()

            case 4:
                if len(job_dict) == 0:

                    print_lock.acquire()
                    print("No jobs active")
                    print_lock.release()

                else:

                    print_lock.acquire()
                    print("\nPick an active monitor job to stop:")
                    print_lock.release()

                    for key, value in job_dict.items():

                        print_lock.acquire()
                        print(key, value)
                        print_lock.release()

                    while True:
                        menu_select = int(prompt("Enter the integer next to the job to stop: "))
                        if menu_select not in range(1, len(job_dict)+1):

                            print_lock.acquire()
                            print('Invalid input, try again')
                            print_lock.release()

                            continue
                        break
                    cancel_job(job_dict, menu_select)
                    job_num -= 1


            case 5:
                monitor_num = add_monitor(monitor_dict, monitor_num, print_lock)

            case 6:
                stop_flag = True

            case _:
                print_lock.acquire()
                print("default action triggered")
                print_lock.release()

        if stop_flag == True:
            break

    print("end of hub")


def add_monitor(monitor_dict, monitor_num, print_lock):

    while True:
        ip_add = prompt('\nEnter the remote monitor server ip address: ')
        port_num = int(prompt('Enter the remote monitor server port number: '))

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip_add, port_num))

        except:

            print_lock.acquire()
            print('\nCould not connect to this server, please try again')
            print_lock.release()

            sock.close()
            continue

        else:
            new_entry = {"uid": ("MON_SERV_" + str(monitor_num)), "ip": ip_add, "port": port_num}
            monitor_dict[monitor_num] = new_entry
            monitor_num += 1
            sock.close()

            next_step = None

            while True:
                add_more = prompt("\nEnter 'add' to input another monitor server or 'quit' to move on: ")
                if add_more.lower() == 'add':
                    next_step = 'loop'
                    break
                elif add_more.lower() == 'quit':
                    next_step = 'exit'
                    break
                else:

                    print_lock.acquire()
                    print('Input not recognized try again')
                    print_lock.release()

                    continue

            if next_step == 'exit':
                break

    return monitor_num


def serv_add(serv_dict, ser_num, print_lock):

    print_lock.acquire()
    print("\nAvailable monitoring types:")
    print("1. http\n" + "2. https\n" + "3. ntp\n" + "4. dns\n" + "5. tcp\n" + "6. udp\n")
    print_lock.release()

    while True:
        target = int(prompt("Enter an integer to select a type: "))
        if target not in [1, 2, 3, 4, 5, 6]:

            print_lock.acquire()
            print('Invalid input, try again.\n')
            print_lock.release()

            continue
        break

    if target == 1:
        input1 = prompt("Input the http address or hostname: ")
        input2 = prompt("Input the http monitoring interval in seconds: ")
        dict_entry = {"type": "http", "address": input1, "interval": input2}
        serv_dict[ser_num] = dict_entry
        ser_num += 1

    elif target == 2:
        input1 = prompt("Input the https address or hostname: ")
        input2 = prompt("Input the https monitoring interval in seconds: ")
        input3 = prompt("Input the https timeout in seconds: ")
        dict_entry = {"type": "https", "address": input1, "interval": input2, "timeout": input3}
        serv_dict[ser_num] = dict_entry
        ser_num += 1

    elif target == 3:
        input1 = prompt("Input the ntp address or hostname: ")
        input2 = prompt("Input the ntp monitoring interval in seconds: ")
        dict_entry = {"type": "ntp", "address": input1, "interval": input2}
        serv_dict[ser_num] = dict_entry
        ser_num += 1

    elif target == 4:
        input1 = prompt("Input the dns server address: ")
        input2 = prompt("Input the dns monitoring interval in seconds: ")
        input3 = prompt("Input the dns query: ")
        input4 = prompt("Input the dns type: ")
        dict_entry = {"type": "dns", "address": input1, "interval": input2, "query": input3, "DNS_type": input4}
        serv_dict[ser_num] = dict_entry
        ser_num += 1

    elif target == 5:
        input1 = prompt("Input the tcp server address: ")
        input2 = prompt("Input the tcp monitoring interval in seconds: ")
        input3 = int(prompt("Input the tcp port: "))
        dict_entry = {"type": "tcp", "address": input1, "interval": input2, "port": input3}
        serv_dict[ser_num] = dict_entry
        ser_num += 1

    elif target == 6:
        input1 = prompt("Input the udp server address: ")
        input2 = prompt("Input the udp monitoring interval in seconds: ")
        input3 = int(prompt("Input the udp port: "))
        dict_entry = {"type": "udp", "address": input1, "interval": input2, "port": input3}
        serv_dict[ser_num] = dict_entry
        ser_num += 1

    return dict_entry, ser_num


def add_job(ser_act, monitor_dict, monitor_num, job_dict, job_num, print_lock):

    serv_dict_entry = ser_act

    print_lock.acquire()
    print("\nPick choose a monitor server to execute this service:")
    print_lock.release()

    for key, value in monitor_dict.items():

        print_lock.acquire()
        print(key, value)
        print_lock.release()

    while True:
        server_selection = int(prompt("\nEnter the integer value to select monitor server: "))
        if server_selection not in range(1, int(monitor_num)):

            print_lock.acquire()
            print("\nCommand invalid, try again.")
            print_lock.release()

            continue
        break

    monitor_dict_entry = monitor_dict[server_selection]

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((monitor_dict_entry['ip'], monitor_dict_entry['port']))

    x = sock.getsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE)
    if x == 0:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

    job_entry = {"service": serv_dict_entry, "server": monitor_dict[server_selection], "sock": sock}
    job_dict[job_num] = job_entry
    job_num += 1

    job_message = ['monitor', monitor_dict_entry['uid']]
    for entry in serv_dict_entry.values():
        job_message.append(entry)
    job_message = str(job_message)


    listen = threading.Thread(daemon=True, target=data_listener, args=(sock, print_lock))
    listen.start()

    send = threading.Thread(daemon=True, target=data_sender, args=(monitor_dict_entry, sock, job_message, print_lock))
    send.start()

    return job_num


def cancel_job(job_dict, job_num):

    job_entry = job_dict.pop(job_num)
    sock = job_entry['sock']
    message = str(['close'])
    sock.sendall(message.encode())
    return

def data_sender(server, sock, message, print_lock):

    sock.sendall(message.encode())
    return


def data_listener(sock, print_lock):

    while True:
        message = sock.recv(1024)
        if message:

            print_lock.acquire()
            print(message.decode())
            print_lock.release()

        else:
            break
    return


def pick_service(serv_dict, print_lock, ser_num):
    print_lock.acquire()
    print("\nPick choose a monitor server to execute this service:")
    print_lock.release()

    for key, value in serv_dict.items():

        print_lock.acquire()
        print(key, value)
        print_lock.release()

    while True:
        input_result = int(prompt("\nEnter the integer value to select monitor server: "))
        if input_result not in range(1, int(ser_num)):

            print_lock.acquire()
            print("\nCommand invalid, try again.")
            print_lock.release()

            continue
        break
    return input_result


if __name__ == "__main__":
    monitor_hub()