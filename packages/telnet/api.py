import sys
import telnetlib
from core.logging.api import info, warning, error

tn_ip = "0.0.0.0"
tn_port = "23"
tn_username = "admin"
tn_password = "admin"

def telnet(host, port, username, password):
    try:
        tn = telnetlib.Telnet(host, port, 15)
    except:
        error("Unable to connect to Telnet server: " + tn_ip)
        return
    tn.set_debuglevel(100)
    tn.read_until("Username: ")
    tn.write(username + "\n")
    tn.read_until("Password: ")
    tn.write(password + "\n")
    tn.read_until("TC>")
    info("TELNET WORKED!")
