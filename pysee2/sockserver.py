import socket
import sys
import os
import threading

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

# Comm In Function
def comm_in(remote_target):
    print('[+] Awaiting response... ')
    response = []
    while True:
        response.append(remote_target.recv(8192).decode())
        if not response[-1]:
            return "".join(response)

# Comm_Out Function
def comm_out(remote_target, message):
    remote_target.send(message.encode())

# Listener Handler Update
def listener_handler():
    sock.bind((host_ip, int(host_port)))
    print('[+] Awaiting connection from client...')
    sock.listen()
    t1 = threading.Thread(target=comm_handler)
    t1.start()
    
# Listener Handler Function
# def listener_handler(host_ip, host_port, targets):
#     sock.bind((host_ip, host_port))
#     print('[+] Awaiting connection from client...')
#     sock.listen()
#     remote_target, remote_ip = sock.accept()
#     targets.append([remote_target, remote_ip])
#     print(targets)
#     print((targets[0])[0])
#     print((targets[0])[1])
#     comm_handler(remote_target, remote_ip)

# Comm_Handler update
def comm_handler():
    while True:
        try:
            remote_target, remote_ip = sock.accept()
            targets.append([remote_target, remote_ip[0]])
            print(f'\n[+] Connection received from {remote_ip[0]}\n' + 'Enter Command#> ', end="")
        except:
            pass


# Comm_Handler function
# def comm_handler(remote_target, remote_ip):
#     print(f'[+] Connection received from {remote_ip[0]}')
#     while True:
#         try:
#             message = input('Message to send#> ')
#             #Exit message handling
#             if message == 'exit':
#                 remote_target.send(message.encode())
#                 remote_target.close()
#                 break
#             remote_target.send(message.encode())
#             response = remote_target.recv(1024).decode()
#             if response == 'exit':
#                 print('[-] Client has terminated the session. Bye bye..')
#                 remote_target.close()
#                 break
#             print(response)
#         except KeyboardInterrupt:
#             print('[-] Keyboard interrupt issued.')
#             message = 'exit'
#             remote_target.send(message.encode())
#             sock.close()
#             break
#         except Exception:
#             remote_target.close()
#             break


if __name__ == '__main__':
    sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=32, cols=200))
    targets = []
    banner()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        #host_ip = sys.argv[1]
        #host_port = int(sys.argv[2])
        host_ip = '127.0.0.1'
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
                    print('Session' + ' ' * 10 + 'Target')
                    for target in targets:
                        print(str(session_counter) + ' ' * 16 + target[1])
                        session_counter += 1
                    if command.split(" ")[1] == '-i':
                        num = int(command.split(" ")[2])
                        targ_id = (targets[num])[0]
                        target_comm(targ_id)
        except KeyboardInterrupt:
            print('\n[-] Keyboard interrupt issued')
            sock.closed
            break




