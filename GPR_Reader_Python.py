import os
import sys
import time
import json
import textwrap
import urllib.request
import urllib.error
from getpass import getpass

# --- Configuration ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "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")
GROQ_MODEL = "llama-3.3-70b-versatile"

# Place your Gemini API key here or set as environment variable GEMINI_API_KEY
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyAtWS9_d_Li40IGVYoT7tQgSiPPiXRv6iU")
GEMINI_MODEL = "gemini-2.5-flash"  # You can change this to your preferred Gemini model

def print_ascii_art():
    print(r"""
________  __________  __________
/  _____/  \______   \ \______   \
/   \  ___   |     ___/  |       _/
\    \_\  \  |    |      |    |   \
 \______  /  |____|      |____|_  /
        \/                      \/

__________                        .___ 
\______   \   ____   _____      __| _/   ____   _______  
 |       _/ _/ __ \  \__  \    / __ |  _/ __ \  \_  __ \ 
 |    |   \ \  ___/   / __ \_ / /_/ |  \  ___/   |  | \/ 
 |____|_  /  \___  > (____  / \____ |   \___  >  |__|    
        \/       \/       \/       \/       \/           

GPR Reader Python edition
""")

def loading_bar(total_seconds=1):
    bar_length = 40
    total_items = 100
    print("\nProgress:")
    for i in range(total_items + 1):
        percent = 100 * i / total_items
        filled_length = int(bar_length * i // total_items)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        print(f"\r|{bar}| {percent:5.1f}% Complete", end='', flush=True)
        time.sleep(total_seconds / total_items)
    print("\n")

def start_chat_groq():
    global GROQ_API_KEY

    if not GROQ_API_KEY or "your_key" in GROQ_API_KEY:
        print("\033[1;33mWarning:\033[0m Groq API Key is not set in environment variable or hardcoded.")
        try:
            key_input = getpass("Please enter your Groq API Key (input is hidden): ")
            if key_input:
                GROQ_API_KEY = key_input
            else:
                print("\033[1;31mError:\033[0m API Key is required to start the chat.")
                return
        except Exception as e:
            print(f"\033[1;31mError during key input:\033[0m {e}")
            return

    print("-" * 52)
    print("Groq Llama3 AI Chat Initialized.")
    print("Type 'exit' or 'quit' to return to the main menu.")
    print("-" * 52)

    api_url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    while True:
        try:
            user_message = input("\033[1;32mYou:\033[0m ")
        except EOFError:
            print("\nExiting chat...")
            break
        except KeyboardInterrupt:
            print("\nExiting chat...")
            break

        if user_message.lower() in ["exit", "quit"]:
            print("Exiting chat...")
            break

        if not user_message.strip():
            continue

        print("Thinking...")

        payload = {
            "model": GROQ_MODEL,
            "messages": [{"role": "user", "content": user_message}]
        }

        req = urllib.request.Request(
            api_url,
            data=json.dumps(payload).encode('utf-8'),
            headers=headers,
            method='POST'
        )

        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                resp_data = response.read().decode('utf-8')
                data = json.loads(resp_data)
        except urllib.error.HTTPError as e:
            try:
                error_data = e.read().decode('utf-8')
                error_json = json.loads(error_data)
                error_msg = error_json.get('error', {}).get('message', str(e))
            except Exception:
                error_msg = str(e)
            print(f"\033[1;31mAPI Error:\033[0m\n{error_msg}")
            continue
        except Exception as e:
            print(f"\033[1;31mNetwork/Request Error:\033[0m {e}")
            continue

        ai_reply = data.get('choices', [{}])[0].get('message', {}).get('content', '').strip()

        if ai_reply:
            print("\033[1;36mGroq:\033[0m")
            try:
                cols = os.get_terminal_size().columns
            except OSError:
                cols = 80
            width = max(20, cols - 2)
            wrapped_text = textwrap.fill(ai_reply, width=width, subsequent_indent='  ')
            print(wrapped_text)
            print()
        else:
            print("\033[1;31mError:\033[0m Received empty reply from API.")
            print(f"Raw Output: {data}")

def start_chat_gemini():
    global GEMINI_API_KEY

    if not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
        print("\033[1;33mWarning:\033[0m Gemini API Key is not set in environment variable or hardcoded.")
        try:
            key_input = getpass("Please enter your Gemini API Key (input is hidden): ")
            if key_input:
                GEMINI_API_KEY = key_input
            else:
                print("\033[1;31mError:\033[0m API Key is required to start the chat.")
                return
        except Exception as e:
            print(f"\033[1;31mError during key input:\033[0m {e}")
            return

    print("--------------------------------")
    print("Google Gemini AI Chat Initialized.")
    print("Type 'exit' or 'quit' to return to the main menu.")
    print("--------------------------------")

    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"

    while True:
        try:
            user_message = input("\033[1;32mYou:\033[0m ")
        except EOFError:
            print("\nExiting chat...")
            break
        except KeyboardInterrupt:
            print("\nExiting chat...")
            break

        if user_message.lower() in ["exit", "quit"]:
            print("Exiting chat...")
            break

        if not user_message.strip():
            continue

        print("Thinking...")

        payload = {
            "contents": [{"parts": [{"text": user_message}]}],
            "systemInstruction": {
                "parts": [{
                    "text": "You are a helpful, brief, and knowledgeable assistant for Ground Penetrating Radar (GPR) analysis. Provide concise answers. Only provide information on GPRs."
                }]
            }
        }

        headers = {
            "Content-Type": "application/json"
        }

        req = urllib.request.Request(
            api_url,
            data=json.dumps(payload).encode('utf-8'),
            headers=headers,
            method='POST'
        )

        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                resp_data = response.read().decode('utf-8')
                data = json.loads(resp_data)
        except urllib.error.HTTPError as e:
            try:
                error_data = e.read().decode('utf-8')
                error_json = json.loads(error_data)
                error_msg = error_json.get('error', {}).get('message', str(e))
            except Exception:
                error_msg = str(e)
            print(f"\033[1;31mAPI Error:\033[0m\n{error_msg}")
            continue
        except Exception as e:
            print(f"\033[1;31mNetwork/Request Error:\033[0m {e}")
            continue

        # Gemini's response structure
        candidate = (data.get("candidates") or [{}])[0]
        ai_reply = ""
        if candidate:
            ai_reply = candidate.get("content", {}).get("parts", [{}])[0].get("text", "").strip()

        if ai_reply:
            print("\033[1;36mGemini:\033[0m")
            try:
                cols = os.get_terminal_size().columns
            except OSError:
                cols = 80
            width = max(20, cols - 2)
            wrapped_text = textwrap.fill(ai_reply, width=width, subsequent_indent='  ')
            print(wrapped_text)
            print()
        else:
            print("\033[1;31mError:\033[0m Received empty reply from API.")
            print(f"Raw Output: {data}")

# --- Main Menu Loop ---
def main():
    print_ascii_art()
    loading_bar(total_seconds=1)

    while True:
        try:
            user_input_terminal = input("Enter 'commands' to obtain functional commands (or Ctrl+C to stop): ").strip().lower()
        except KeyboardInterrupt:
            print("\nExiting GPR Reader. Goodbye!")
            sys.exit(0)
        except EOFError:
            print("\nExiting GPR Reader. Goodbye!")
            sys.exit(0)

        if user_input_terminal in ["help", "commands"]:
            print("\nAvailable Commands:")
            print("read_gpr       - Read and process GPR files.")
            print("analyze_data   - Analyze the processed data.")
            print("export_results - Export the results to a file.")
            print("exit           - Exit the GPR Reader Python edition.")
            print("commands       - Display this message with available commands.")
            print("chat groq      - Chat with Groq AI")
            print("chat gemini    - Chat with Google Gemini AI")
            print("help           - Helps you to overcome problems you are facing with this CLI")
            print("version        - Show version information.")
            print("Enter a command to get started.")

        elif user_input_terminal == "chat groq":
            start_chat_groq()

        elif user_input_terminal == "chat gemini":
            start_chat_gemini()

        elif user_input_terminal == "exit":
            print("Exiting GPR Reader. Goodbye!")
            sys.exit(0)

        elif user_input_terminal in ["read_gpr", "analyze_data", "export_results"]:
            print(f"'{user_input_terminal}' is not implemented yet in this Python script.")
        elif user_input_terminal == "version":
            print("GPR Reader Python edition - Version 1.0.0")

        else:
            print("Invalid input. Please enter 'commands' to see available commands.")

        print()

if __name__ == "__main__":
    main()


    