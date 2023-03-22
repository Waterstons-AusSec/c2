import socket
import sys
import os

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
    response = remote_target.recv(1024).decode()
    return response

# Comm_Out Function
def comm_out(remote_target, message):
    remote_target.send(message.encode())

# Listener Handler Function
def listener_handler():
    sock.bind((host_ip, host_port))
    print('[+] Awaiting connection from client...')
    sock.listen()
    remote_target, remote_ip = sock.accept()
    comm_handler(remote_target, remote_ip)

# Comm_Handler function
def comm_handler(remote_target, remote_ip):
    print(f'[+] Connection received from {remote_ip[0]}')
    while True:
        try:
            message = input('Message to send#> ')
            #Exit message handling
            if message == 'exit':
                remote_target.send(message.encode())
                remote_target.close()
                break
            remote_target.send(message.encode())
            response = remote_target.recv(1024).decode()
            if response == 'exit':
                print('[-] Client has terminated the session. Bye bye..')
                remote_target.close()
                break
            print(response)
        except KeyboardInterrupt:
            print('[-] Keyboard interrupt issued.')
            remote_target.close()
            break
        except Exception:
            remote_target.close()
            break


if __name__ == '__main__':  
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_ip = sys.argv[1]
    host_port = int(sys.argv[2])
    banner()
    listener_handler()

