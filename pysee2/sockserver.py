import socket
import sys

def listener_handler():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host_ip, host_port))
    print('[+] Awaiting connection from client...')
    sock.listen()
    remote_target, remote_ip = sock.accept()
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

host_ip = sys.argv[1]
host_port = int(sys.argv[2])
listener_handler()

