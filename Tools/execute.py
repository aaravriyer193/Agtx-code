from types import SimpleNamespace
import subprocess

dangerous_commands = [
    "rm", "rmdir", "del", "erase", "format", "mkfs", "dd", "chmod", "chown", "mv", "move", "cp", "copy",
    "ln", "apt", "apt-get", "dpkg", "yum", "dnf", "pacman", "zypper", "brew", "pip", "npm", "systemctl",
    "service", "init", "shutdown", "reboot", "poweroff", "kill", "pkill", "killall", "taskkill", "passwd",
    "userdel", "groupdel", "fdisk", "parted", "gparted", "shred", "wipe", "tune2fs", "chattr", "reg", "net",
    "sc", "netsh", "vssadmin", "wbadmin", "bcdedit", "Remove-Item", "Stop-Process", "Stop-Service",
    "Restart-Computer", "Stop-Computer", "Clear-Disk", "Format-Volume", "Set-ExecutionPolicy"
]

def execute_command(agentoutput, chat_messages, homelocation, timeout_val=30):
    BLUE, RESET = '\033[34m', '\033[0m'
    rawagentoutput = agentoutput
    agentoutput = agentoutput.split("<tool:call execute_terminal_command>")[1]
    currenttool = agentoutput.split("</tool:call execute_terminal_command>")[0].strip()
    currentmsg = rawagentoutput.split("<tool:call execute_terminal_command>")[0]
    
    print("\n" + currentmsg.strip())
    
    if any(cmd in currenttool.split() for cmd in dangerous_commands):
        decision = input(f"\nDangerous command intercepted: {BLUE}{currenttool}{RESET}\nApprove run? (y/n): ")
        if decision.lower() != "y":
            chat_messages.append({"role": "user", "content": "Execution Blocked: Command was rejected by the supervisor security gate."})
            return SimpleNamespace(chat_messages=chat_messages)
            
    print("Executing... " + currenttool)
    try: 
        output = subprocess.run(currenttool, shell=True, capture_output=True, text=True, cwd=homelocation, timeout=timeout_val)
        output = str(output.stdout + output.stderr)
    except subprocess.TimeoutExpired:
        output = f"Execution timed out safely after exceeding maximum boundary cap of {timeout_val} seconds."
    except Exception as e:
        output = f"Runtime operational error: {str(e)}"
        
    chat_messages.append({"role": "user", "content": f"Command executed output stream result:\n{output}"})
    return SimpleNamespace(chat_messages=chat_messages)