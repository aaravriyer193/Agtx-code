from types import SimpleNamespace

def read_file(agentoutput, chat_messages):
    BLUE, RESET = '\033[34m', '\033[0m'
    rawagentoutput = agentoutput
    currentmsg = rawagentoutput.split("<tool:call read_file>")[0]
    print("\n" + currentmsg.strip())
    
    agentoutput = agentoutput.split("<tool:call read_file>")[1]
    currenttool = agentoutput.split("</tool:call read_file>")[0]
    filename = currenttool.split("<name>")[1].split("</name>")[0].strip()
    
    print(f"{BLUE}Reading{RESET} | " + filename)
    try:
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()
    except FileNotFoundError:
        content = "File is non-existent" 
        
    prompt = f"The file you requested was called: {filename} with the content: \n{content}"
    chat_messages.append({"role": "user", "content": prompt})
    return SimpleNamespace(chat_messages=chat_messages)