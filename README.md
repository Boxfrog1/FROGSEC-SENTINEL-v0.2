# FROGSEC-SENTINEL-v0.2

 FrogSec Sentinel v0.2 — Low-level Android monitor for Termux. Uses Nucleus Binding &amp; Entropy Vectors to detect how exposed your device is.
 
FrogSec Sentinel v0.2

This tool helps you check how "clean" or "watched" your Android phone is.
It quietly looks at different parts of your phone's system and gives you a simple score that tells you how safe your device feels. Think of it like a security check-up for your phone.


How to Install It Correctly (Very Important)

Step 1: Install Termux the right way
Do NOT download Termux from the Play Store.
Go to your browser and visit: https://f-droid.org
Search for "Termux" and install it from there.

Step 2: Set up FrogSec Sentinel
Open Termux and type these commands one by one:
pkg update && pkg upgrade -y
pkg install python git -y
git clone https://github.com/Boxfrog1/FROGSEC-SENTINEL-v0.2.git
cd FROGSEC-SENTINEL-v0.2
python sentinel.py

The program will now run and show you a colored box with your phone's "Affinity Score".
GREEN = CLEAN → Your phone looks good
RED = WARNING → Something looks suspicious
To stop it, just press Ctrl + C on your keyboard.
