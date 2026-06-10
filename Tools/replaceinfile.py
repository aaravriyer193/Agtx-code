from types import SimpleNamespace
import re

def replace_in_file(agentoutput, chat_messages):
    BLUE, RESET = '\033[34m', '\033[0m'
    rawagentoutput = agentoutput
    agentoutput = agentoutput.split("<tool:call replace_in_file>")[1]
    currenttool = agentoutput.split("</tool:call replace_in_file>")[0]
    currentmsg = rawagentoutput.split("<tool:call replace_in_file>")[0]
    
    filename = currenttool.split("<name>")[1].split("</name>")[0].strip()
    old_content = currenttool.split("<old>")[1].split("</old>")[0].strip('\r\n')
    new_content = currenttool.split("<new>")[1].split("</new>")[0]
    
    print("\n" + currentmsg.strip())
    print(f"{BLUE}Patching{RESET} | " + filename)
    
    try:
        with open(filename, "r", encoding="utf-8") as file:
            file_data = file.read()
            
        escaped_old = re.escape(old_content.strip())
        flexible_regex = re.sub(r'\\\s+', r'\\s*', escaped_old)
        match = re.search(flexible_regex, file_data)
        
        if match:
            start, end = match.span()
            updated_data = file_data[:start] + new_content + file_data[end:]
            with open(filename, "w", encoding="utf-8") as file:
                file.write(updated_data)
            prompt = f"File {filename} successfully patched."
        else:
            prompt = f"Error: Specified <old> code block could not be matched exactly inside {filename}. Verify whitespaces/indentation."
    except Exception as e:
        prompt = f"Patch execution failed: {str(e)}"
        
    chat_messages.append({"role": "user", "content": prompt})
    return SimpleNamespace(chat_messages=chat_messages)