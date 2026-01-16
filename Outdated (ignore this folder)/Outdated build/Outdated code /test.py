import os
import time
from ez_background_music import start_music, stop_music

# 1. Get the absolute path to your music file
# This ensures it works even if you run the script from a different folder
script_dir = os.path.dirname(os.path.abspath(__file__))
audio_file = os.path.join(script_dir, "/Users/Anay_Rustogi/Desktop/Mystery Miners - GPR Reader/Python_edition/GPR_Reader_Python_Edition_v3/Incredulity-chosic.com_.mp3")

def run_my_app():
    print("Initializing GPR Hub...")
    
    # 2. Start the music in the background
    success = start_music(audio_file)
    
    if success:
        print("🎵 Background music started!")
    else:
        print("⚠️ Music failed to start (check file path).")

    # 3. Your app logic runs here
    print("SUPPOSED") 
    time.sleep(5) # Simulating your app running
    
    # 4. Stop the music before exiting
    stop_music()
    print("App closed.")

if __name__ == "__main__":
    run_my_app()