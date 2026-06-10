from Utils.apicall import api_call as apicall
from Utils.prompts import sysprompt
from Tools.createfile import create_file
from Tools.readfile import read_file
from Tools.execute import execute_command
from Tools.replaceinfile import replace_in_file
from Tools.presentfiles import present_files
from Tools.gitmanager import git_manager

import os
import json
import subprocess
import threading

SETTINGS_FILE = "settings.json"

RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
RESET = '\033[0m'

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {"openrouter_api_key": "", "working_directory": "", "model": "xiaomi/mimo-v2.5-pro", "terminal_timeout": 30}

def main():
    print(f"\n\n {RESET} === WELCOME TO {BLUE} ✦ Agtx {RESET} === {BLUE}")
    print(r""" _______  _______ _________         
(  ___  )(  ____ \\__   __/|\     /|
| (   ) || (    \/   ) (   ( \   / )
| (___) || |         | |    \ (_) / 
|  ___  || | ____    | |     ) _ (  
| (   ) || | \_  )   | |    / ( ) \ 
| )   ( || (___) |   | |   ( /   \ )
| |    \|(_______)   )_(   |/     \|
| \_________________________________
\___________________________________\                                
""")

    settings = load_settings()
    api_key = settings.get("openrouter_api_key", "").strip()
    homelocation = settings.get("working_directory", "").strip()
    selected_model = settings.get("model", "xiaomi/mimo-v2.5-pro").strip()
    timeout_val = settings.get("terminal_timeout", 30)

    while not api_key:
        print(f"{YELLOW}No OpenRouter API key found in settings.{RESET}")
        api_key = input(f"Please enter your {BLUE}OpenRouter API Key{RESET}: ").strip()
        if not api_key:
            continue
            
        with open(SETTINGS_FILE, "w") as f:
            json.dump({
                "openrouter_api_key": api_key,
                "working_directory": homelocation,
                "model": selected_model,
                "terminal_timeout": timeout_val
            }, f, indent=4)

    current_working_dir = os.getcwd()
    if not homelocation or not os.path.exists(homelocation):
        print(f"\nCurrent path: {YELLOW}{current_working_dir}{RESET}")
        use_current = input(f"Use this directory? {BLUE}(y/n){RESET}: ").lower()
        if use_current == 'y':
            homelocation = current_working_dir
        else:
            while not homelocation or not os.path.exists(homelocation):
                homelocation = input(f"Enter your {BLUE}working directory path{RESET}: ").strip()
                if not os.path.exists(homelocation):
                    print(f"{RED}Directory not found.{RESET}")
                    
        with open(SETTINGS_FILE, "w") as f:
            json.dump({
                "openrouter_api_key": api_key,
                "working_directory": homelocation,
                "model": selected_model,
                "terminal_timeout": timeout_val
            }, f, indent=4)

    os.chdir(homelocation)
    ls_cmd = ["powershell", "-Command", "ls"] if os.name == 'nt' else ["ls"]
    homelocationlsresult = subprocess.run(ls_cmd, capture_output=True, text=True, shell=True)
    filesinwd = homelocationlsresult.stdout

    print(f"\n{GREEN}--- Files in Directory ---{RESET}")
    print(filesinwd)
    
    confirm = input(f"Continue with this directory? {BLUE}(y/n){RESET}: ").lower()
    if confirm != "y":
        print(f"{RED}Exiting.{RESET}")
        return

    if not selected_model:
        selected_model = input(f"Enter OpenRouter {BLUE}model name{RESET} (Default: xiaomi/mimo-v2.5-pro): ").strip()
        if not selected_model:
            selected_model = "xiaomi/mimo-v2.5-pro"
            
        with open(SETTINGS_FILE, "w") as f:
            json.dump({
                "openrouter_api_key": api_key,
                "working_directory": homelocation,
                "model": selected_model,
                "terminal_timeout": timeout_val
            }, f, indent=4)

    print(f"\n--- {GREEN}Agtx is Ready{RESET} ---")
    print(f"Directory: {homelocation}\nModel: {selected_model}\nTimeout: {timeout_val}s\n")

    chat_messages = [{"role": "system", "content": sysprompt}]

    while True:
        user_input = input(f"{BLUE}You: {RESET}")
        finished = False
        
        prompt = f"These are all the files in your working directory:\n{filesinwd}\n\nThe user has this query: {user_input}\nbegin working, the user will not be reachable until the edits are done."
        chat_messages.append({"role": "user", "content": prompt})
        
        while not finished:
            stop_loading = threading.Event()
            frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
            
            def spin():
                import sys, time
                i = 0
                while not stop_loading.is_set():
                    sys.stdout.write(f"\r{BLUE}{frames[i % len(frames)]} {RESET}Thinking...")
                    sys.stdout.flush()
                    i += 1
                    time.sleep(0.1)
                sys.stdout.write("\r" + " " * 30 + "\r")
                sys.stdout.flush()
                
            loader_thread = threading.Thread(target=spin)
            loader_thread.start()
            
            try:
                agentoutput, chat_messages = apicall(model=selected_model, messages=chat_messages)
            finally:
                stop_loading.set()
                loader_thread.join()
                
            if agentoutput is None or agentoutput.startswith("Error:") or agentoutput.startswith("API Error") or agentoutput.startswith("Network Error"):
                print(f"\n{RED}Stopped: {agentoutput}{RESET}\n")
                break
            
            if "<tool:call create_file>" in agentoutput:
                chat_messages = create_file(agentoutput, chat_messages).chat_messages
                
            elif "<tool:call replace_in_file>" in agentoutput:
                chat_messages = replace_in_file(agentoutput, chat_messages).chat_messages
                
            elif "<tool:call read_file>" in agentoutput:
                chat_messages = read_file(agentoutput, chat_messages).chat_messages
                
            elif "<tool:call present_files" in agentoutput:
                chat_messages = present_files(agentoutput, chat_messages, homelocation).chat_messages
                
            elif "<tool:call git_action>" in agentoutput:
                chat_messages = git_manager(agentoutput, chat_messages, homelocation).chat_messages
                
            elif "<tool:call execute_terminal_command>" in agentoutput:
                chat_messages = execute_command(agentoutput, chat_messages, homelocation, timeout_val).chat_messages
                
            elif "<agtx:complete>" in agentoutput:
                finished = True
                currentmsg = agentoutput.replace("<agtx:complete>", "")
                print(currentmsg.strip() + "\n")

if __name__ == "__main__":
    main()