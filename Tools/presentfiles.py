from types import SimpleNamespace
import subprocess
import os

def present_files(agentoutput, chat_messages, homelocation):
    BLUE, RESET = '\033[34m', '\033[0m'
    rawagentoutput = agentoutput
    currentmsg = rawagentoutput.split("<tool:call present_files>")[0] if "<tool:call present_files>" in rawagentoutput else rawagentoutput.split("<tool:call present_files />")[0]
    
    print("\n" + currentmsg.strip())
    print(f"{BLUE}Presenting Workspace Structure Tree...{RESET}")
    
    try:
        if os.name == 'nt':
            cmd = ["powershell", "-Command", "Get-ChildItem -Recurse -Depth 4 | Where-Object { $_.FullName -notmatch 'node_modules|\\.git|\\.next' } | Select-Object FullName"]
        else:
            cmd = ["find . -maxdepth 4 -not -path '*/.*' -not -path '*node_modules*' -not -path '*.next*'"]
            
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=homelocation, shell=True)
        output = result.stdout if result.stdout else "Directory empty or command layout error."
    except Exception as e:
        output = f"Tree mapping error: {str(e)}"
        
    prompt = f"This is the current file structural map of the workspace:\n{output}"
    chat_messages.append({"role": "user", "content": prompt})
    return SimpleNamespace(chat_messages=chat_messages)