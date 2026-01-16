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


import matplotlib.pyplot as plt
import numpy as np

def process_gpr_image(file_path):
    """
    Reads and processes the image data from the given path.
    The image is converted to a 2D intensity array (grayscale) suitable 
    for GPR analysis.
    """
    if not os.path.exists(file_path):
        print(f"❌ Error: File not found at path: {file_path}")
        return None
        
    try:
        # 1. Read the image into a NumPy array
        img_data = plt.imread(file_path)
        
        print(f"✅ Image loaded successfully from: {os.path.basename(file_path)}")
        print(f"Shape of the original data: {img_data.shape}")
        
        # 2. Pre-processing: Convert to Grayscale (Intensity)
        
        # Drop the alpha channel if present (4 channels -> 3 channels)
        if img_data.ndim == 3 and img_data.shape[2] == 4:
            img_data = img_data[:, :, :3]
            
        # Convert to Grayscale if it's a color image (3 channels -> 1 channel)
        if img_data.ndim == 3:
            # Standard luminance formula for grayscale conversion
            # Resulting array is 2D (Depth vs. Distance)
            gray_data = np.dot(img_data[...,:3], [0.2989, 0.5870, 0.1140])
            print("Converted image to Grayscale (2D array) for processing.")
            return gray_data
        
        # If it was already 1 channel (grayscale), return it directly
        return img_data

    except Exception as e:
        print(f"❌ An error occurred while reading the file: {e}")
        return None

# --- Main Script Loop ---

def gpr_reader_cli_run():
    """Main command-line interface for the GPR reader."""
    gpr_array = None
    
    print("Welcome to the GPR Image Reader.")
    print("Type 'upload <file_path>' to load an image, or 'exit' to quit.")
    print("Make sure that the name of the file does not contain spaces.")
    print("\n💡 **Examples:**")
    print("   Windows: upload C:\\Data\\profile.png")
    print("   Linux/macOS: upload /home/user/data/profile.png")
    
    while True:
        user_input = input("\n> ").strip()
        
        # 1. Handle the 'exit' command
        if user_input.lower() == 'exit':
            print("Exiting GPR Reader. Goodbye!")
            break
            
        # 2. Handle the 'upload <file_path>' command
        if user_input.lower().startswith('upload '):
            # Split the input into the command and the path
            parts = user_input.split(maxsplit=1)
            
            if len(parts) < 2:
                print("⚠️ Please provide the full path after 'upload'.")
                continue
            
            # Remove any extra quotes the user might have included
            file_path = parts[1].strip().replace('"', '').replace("'", '')
            
            # Call the processing function
            gpr_array = process_gpr_image(file_path)
            
            if gpr_array is not None:
                print("\n**Image successfully loaded and processed.**")
                
                # Show the result for confirmation
                plt.figure()
                plt.imshow(gpr_array, cmap='gray', aspect='auto')
                plt.title("Loaded GPR Profile (Intensity)")
                plt.xlabel("Distance Axis (Pixels)")
                plt.ylabel("Depth/Time Axis (Pixels)")
                plt.colorbar(label='Amplitude/Intensity')
                plt.show()
                





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
    print ("If you face any issues, seek help from the github repository (https://github.com/Codemaster-AR/GPR_Reader_Identify_Python_Beta). If that does not work, you can contact codemaster.ar@gmail.com")
    print ("Also, if you face any issues regarding the imports, you can re-run this CLI and type help after the ascii title art is shown to get help regarding the issues you are facing.")
    print ("----------------------------------------------------------------------------------------------------------------")
    print ("You must grant permission for this script to access files on your system for it to work properly. This python script is completely safe and does not store or share any of your data. It only processes the files locally on your system, but DO NOT share sensitive files with this script as it is sent to Gemini using API keys. Only share GPR images. Make sure that this file was downloaded from the github repository (link above) for security purposes.")
    print ("Granting per§mission commands:")
    print(" Windows: Right-click this file, select Properties, go to the Security tab, and ensure your user account or the \"Users\" group has a checkmark in the Read permission box. Click Apply and OK to save changes.")
    print(" Linux/macOS: Open a terminal and run the following commands:")
    print("1. locate to the file: cd /path/to/directory/containing/GPR_Reader_Python.py")
    print("2. chmod +r GPR_Reader_Python.py")


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

        if user_input_terminal in ["commands"]:
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

        elif user_input_terminal in ["analyze_data", "export_results"]:
            print(f"'{user_input_terminal}' is not implemented yet in this Python script.")
        elif user_input_terminal == "version":
            print("GPR Reader Python edition - Version 1.0.0")
        elif user_input_terminal == "help":
            print("Python edition help:")
            print ("Ensure that you have python3 installed on your system.")
            print("Any errors such as 'module not found' indicate missing dependencies or typos. Make sure that you have python3 installed along with required libraries. You can install the following libraries using '!pip3 install <library_name>'")
            print("Check the GitHub repository for detailed instructions for installing python3")
            print("The required libraries are already a part of default python3 installation, but in case you face any issues, you can install or check their installation status manually.")
            print("Run the following commands in your terminal ")
            print("1. pip3 install os")
            print("2. pip3 install sys")
            print("3. pip3 install time")
            print("4. pip3 install json")
            print("5. pip3 install textwrap")
            print("6. pip3 install urllib")
            print("7. pip3 install urllib.request")
            print("8. pip3 install urllib.error")
            print("9. pip3 install getpass")
            print("10. pip3 install matplotlib")
            print("11. pip3 install numpy")
            print("12. pip3 install -q -U google-genai")
            print("13. pip3 install google")
            print ("14. pip3 install genai")
            print("If you face any other issues, seek help from the github repository (https://github.com/Codemaster-AR/GPR_Reader_Identify_Python_Beta/blob/main/README.md), you can also contact codemaster.ar@gmail.com for further assistance.")
        elif user_input_terminal == "read_gpr":
            gpr_reader_cli_run()
        elif user_input_terminal == "debug":
            import debuggererrortest as debuggererroring
            debuggererroring

        else:
            print("Invalid input. Please enter 'commands' to see available commands.")

        print()

if __name__ == "__main__":
    main()

# Command: python3 GPR_Reader_Python.py
# Note: Ensure you have Python 3.x installed along with required, external libraries: matplotlib, numpy
# import googlegenerativeai
# pip install googlegenerativeai
# !pip3 install googlegenerativeai
                
