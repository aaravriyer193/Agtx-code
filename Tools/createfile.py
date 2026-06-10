from types import SimpleNamespace
import os

def create_file(agentoutput, chat_messages):
    BLUE, RESET = '\033[34m', '\033[0m'
    rawagentoutput = agentoutput
    agentoutput = agentoutput.split("<tool:call create_file>")[1]
    currenttool = agentoutput.split("</tool:call create_file>")[0]
    currentmsg = rawagentoutput.split("<tool:call create_file>")[0]
    
    filename = currenttool.split("<name>")[1].split("</name>")[0].strip()
    filecontent = currenttool.split("<content>")[1].split("</content>")[0]
    
    dirname = os.path.dirname(filename)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
        
    with open(filename, "w", encoding="utf-8") as file:
        file.write(filecontent)
        
    print("\n" + currentmsg.strip())
    print(f"{BLUE}Creating{RESET} | " + filename)
    
    prompt = f"File created: {filename}"
    chat_messages.append({"role": "user", "content": prompt})
    return SimpleNamespace(chat_messages=chat_messages)