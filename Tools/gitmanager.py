from types import SimpleNamespace
import subprocess

def git_manager(agentoutput, chat_messages, homelocation):
    BLUE, RESET = '\033[34m', '\033[0m'
    rawagentoutput = agentoutput
    agentoutput = agentoutput.split("<tool:call git_action>")[1]
    currenttool = agentoutput.split("</tool:call git_action>")[0]
    currentmsg = rawagentoutput.split("<tool:call git_action>")[0]
    
    action = currenttool.split("<action>")[1].split("</action>")[0].strip()
    commit_msg = currenttool.split("<message>")[1].split("</message>")[0].strip() if "<message>" in currenttool else "Agtx Auto-Commit"
    
    print("\n" + currentmsg.strip())
    print(f"{BLUE}Git Version Control Engine:{RESET} | {action}")
    
    try:
        if action == "status":
            cmd = "git status"
        elif action == "commit":
            subprocess.run("git add .", shell=True, cwd=homelocation, capture_output=True)
            cmd = f'git commit -m "{commit_msg}"'
        elif action == "rollback":
            cmd = "git reset --hard HEAD"
        else:
            cmd = "echo 'Invalid SCM request operation.'"
            
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=homelocation)
        output = str(result.stdout + result.stderr)
    except Exception as e:
        output = f"SCM processing breakdown: {str(e)}"
        
    prompt = f"Git tracking action [{action}] execution output:\n{output}"
    chat_messages.append({"role": "user", "content": prompt})
    return SimpleNamespace(chat_messages=chat_messages)