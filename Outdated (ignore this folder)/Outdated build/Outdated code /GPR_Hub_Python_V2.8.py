import os
import sys
import time
import json
import textwrap
import urllib.request
import urllib.error
from getpass import getpass
import matplotlib.pyplot as plt
import numpy as np
from google import genai
from google.genai import types
import webbrowser
from colorama import init, Fore, Style
from cinetext import cinetext_clear, cinetext_type, cinetext_glitch, cinetext_rainbow, cinetext_pulse
import keyboard 
from KeyboardGate import KeyboardGate



def openweb(link):
    webbrowser.open(link)


# Groq Config #
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "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")
GROQ_MODEL = "llama-3.3-70b-versatile"

# Gemini Config #
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyA103EFKpNIQD3tXNLQwCJJiGJ_3dHQ1ls")
GEMINI_MODEL = "gemini-2.5-flash"  # You can change this to your preferred Gemini model

def clear_screen():
    """Clears the console screen."""
    
    os.system('cls' if os.name == 'nt' else 'clear')

def gemini_image_reader():
    YOUR_API_KEY = "AIzaSyC7Y4W06hbx8sUeWzxK168fKoVaJjjjXNw"
    try:
        
        client = genai.Client(api_key=YOUR_API_KEY)
    except Exception as e:
        print("--- API KEY ERROR ---")
        print("Failed to initialize the Gemini client. Ensure your hardcoded key is correct.")
        print(f"Original Error: {e}")
        exit()

    print("Gemini GPR Image Analyzer:")
    print("Please make sure that you paste the pure path to your image file, without any extra quotes (' ' or \" \") or spaces.")
    image_path = input("Please enter the full path to your image file (e.g., /users/anay/radargram.png): ")

# Read, determine
    try:
        # Enable binary mode
        with open(image_path, 'rb') as f:
            image_bytes = f.read()
    
        # Determine type based on file extension
        file_extension = os.path.splitext(image_path)[1].lower()
        if file_extension in ('.jpg', '.jpeg'):
            mime_type = 'image/jpeg'
        elif file_extension == '.png':
            mime_type = 'image/png'
        else:
            # Default to JPEG if not PNG or JPEG, or if the extension is unusual
            print(f"Warning: Unknown file type '{file_extension}'. Using image/jpeg as default MIME type.")
            mime_type = 'image/jpeg'

    except FileNotFoundError:
        print(f"\nError: The file was not found at '{image_path}'. Please check the path and try again.")
        return
    except Exception as e:
        print(f"\nAn unexpected error occurred while reading the file: {e}")
        return

# --- 4. Define the Detailed Prompt ---
    gpr_prompt = (
        "Analyze this image in detail. If it is a Ground-Penetrating Radar (GPR) radargram, "
        "identify any clear hyperbolic reflections, their relative depth/location, and "
        "suggest the potential subsurface objects or features (e.g., rebar, pipe, void). "
        "If it is not a GPR image, simply describe its contents."
    )

    # --- 5. Generate Content ---
    print("\n--- Sending Request to Gemini API... ---")
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[
            types.Part.from_bytes(
                data=image_bytes,
                mime_type=mime_type, 
            ),
            gpr_prompt
        ]
    )

    # --- 6. Print Result ---
    print("\n====================================")
    print("       ✨ GEMINI ANALYSIS RESULT ✨       ")
    print("====================================")
    print(response.text)
    print("====================================")

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
    os.system('cls' if os.name == 'nt' else 'clear')
    logo = r"""
  ____ ____  ____    _   _       _         
 / ___|  _ \|  _ \  | | | |_   _| |__      
| |  _| |_) | |_) | | |_| | | | | '_ \ 
| |_| |  __/|  _ <  |  _  | |_| | |_) |  Python CLI Edition
 \____|_|   |_| \_\ |_| |_|\__,_|_.__/ 
                                                        
    """
    
    cinetext_rainbow(logo, 0.1)
    os.system('cls' if os.name == 'nt' else 'clear')
    cinetext_pulse(logo, 2, 0.05)
    os.system('cls' if os.name == 'nt' else 'clear')
    os.system('cls' if os.name == 'nt' else 'clear')
    os.system('cls' if os.name == 'nt' else 'clear')
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Fore.GREEN}{logo}{Style.RESET_ALL}")
    time.sleep(2)   
    text = (f"GPR Hub Python edition - CLI")
    cinetext_type(text, 0.01)
    time.sleep(1)
    text = (f"Version: 3")
    cinetext_type(text, 0.005)
    time.sleep(1)
    print (" ")
    text = (f"Ensure that your terminal is in fullscreen. ")
    cinetext_pulse(text, 3, 0.05)
    print (" ")
    print (" ")
    time.sleep(0.5)
    text = (f"{Style.RESET_ALL}If you face any issues, seek help from the GitHub repository {Fore.BLUE}(https://github.com/Codemaster-AR/GPR_Reader_Identify_Python_Beta){Style.RESET_ALL}.")
    cinetext_type(text, 0.005)
    text = (f"You can also contact {Fore.BLUE}codemaster.ar@gmail.com {Style.RESET_ALL}for more details or troubleshooting.")
    cinetext_type(text, 0.005)
 


def loading_bar(total_seconds=1):
    bar_length = 40
    total_items = 100
    print(f"{Fore.MAGENTA}\nProgress:")
    for i in range(total_items + 1):
        percent = 100 * i / total_items
        filled_length = int(bar_length * i // total_items)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        print(f"\r|{bar}| {percent:5.1f}% Complete", end='', flush=True)
        time.sleep(total_seconds / total_items)
    print(f"{Style.RESET_ALL}\n")

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
    gate = KeyboardGate()
    gate.KeyboardGateDisable()
    print_ascii_art()
    loading_bar(total_seconds=1)
    gate.KeyboardGateEnable()
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
            print(f"\n{Style.BRIGHT}Available Commands: {Style.NORMAL}")
            print("open_gpr       - Open the GPR image file in a graph format.")
            print("gemini_gpr     - Allow gemini to see the GPR image and analyze it.")
            print("read_gpr       - Read and process GPR files.")
            print("exit           - Exit the GPR Reader Python edition.")
            print("commands       - Display this message with available commands.")
            print("chat groq      - Chat with Groq AI")
            print("chat gemini    - Chat with Google Gemini AI")
            print("gui_ml_gpr     - Opens the GUI website for a machine learning based GPR determiner - tries to determine the object detected in the gpr scan. ")
            print("text_ml_gpr    - Opens the text based machine learning gpr determiner right here.")
            print("help           - Helps you to overcome problems you are facing with this CLI")
            print("version        - Show version information.")
            print("clear          - Clear the terminal screen.")
            print("Enter a command to get started. \nCommands are case sensitive.")

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
            print("GPR Reader Python edition - Version 3.0.0")
            print ("Changelog:")
            print ("Renamed from GPR Reader to GPR Hub, logo changed accordingly.")
            print ("Added new AI Feature")

            print ("Cleaned text interace")
        elif user_input_terminal in ["help", "debug"]:
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
            print("14. pip3 install genai")
            print("15. print install colorama")
            print ("You must grant permission for this script to access files on your system for it to work properly. This python script is completely safe and does not store or share any of your data. It only processes the files locally on your system, but DO NOT share sensitive files with this script as it is sent to Gemini using API keys. Only share GPR images. Make sure that this file was downloaded from the github repository (link above) for security purposes.")
            print ("Granting per§mission commands:")
            print(" Windows: Right-click this file, select Properties, go to the Security tab, and ensure your user account or the \"Users\" group has a checkmark in the Read permission box. Click Apply and OK to save changes.")
            print(" Linux/macOS: Open a terminal and run the following commands:")
            print("1. locate to the file: cd /path/to/directory/containing/GPR_Reader_Python.py")
            print("2. chmod +r GPR_Reader_Python.py")
            print("If you face any other issues, seek help from the github repository (https://github.com/Codemaster-AR/GPR_Reader_Identify_Python_Beta/blob/main/README.md), you can also contact codemaster.ar@gmail.com for further assistance.")
        elif user_input_terminal == "open_gpr":
            gpr_reader_cli_run()
        elif user_input_terminal == "gemini_gpr":
            gemini_image_reader()
        elif user_input_terminal == "clear":
            clear_screen()
        elif user_input_terminal == "gui_ml_gpr":
            print("Opening the ML GPR Analyzer website in your default browser...")
            openweb("https://codemaster-ar.github.io/gpr.demo.determiner/")
        elif user_input_terminal == "text_ml_gpr":
            print("Feature under development - coming soon! Try the GUI version meanwhile by entering the 'gui_ml_gpr' command!")
        elif user_input_terminal == "about_gpr":
            print ("GPR are powerful tools that scan the underground without contact, hence mapping it without the risk of damaging the enviorment, or possibly, any artifacts.")

        else:
            print("Invalid input. Please enter 'commands' to see available commands.")

        print()

if __name__ == "__main__":
    clear_screen()
    main()


# Command: python3 GPR_Reader_Python.py 
# Note: Ensure you have Python 3.x installed along with required, external libraries: matplotlib, numpy
# import googlegenerativeai
# pip install googlegenerativeai
# !pip3 install googlegenerativeai
                


