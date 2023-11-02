################################################################

# File: __init__.py
# Author: Satyam Pandey
# Date: 2023-11-02
# Description: This is a Python script for running the automation
#              in multiple STB simultaneously.

################################################################
import itachIP2IR
import time
import sys
import threading
import signal
import keyboard  # Import the keyboard module for key press detection

# List of keys to be used by keyPress
# p=power,space=select,Return=select,u=menu,v=vod,g=guide,i=info,
# f=fav,d=list,l=last,e=live,a=a,b=b,c=c,w=swap,r=record,x=stop,
# m=mute,Prior=pageup,Next=pagedown,greater=volumeup,less=volumedown,
# bracketright=dayforward,bracketleft=dayback,comma=rewind,slash=play,
# semicolon=pause,period=fastforward,Escape=exit,plus=channelup,
# minus=channeldown,Up=arrowup,Down=arrowdown,Left=arrowleft,Right=arrowright


Pressedkeys = ["g", "Escape", "plus", "minus"]
exit_flag = False

def worker(arg):
    itach_obj = itachIP2IR.itach()
    print("Automation started on itach: " + arg)

    while not exit_flag:
        itach_obj.getData(arg)
        for keys in Pressedkeys:
            itach_obj.OnKeyPress(keys)
            time.sleep(1)

def signal_handler():
    global exit_flag
    exit_flag = True
    print("Exiting the program.")

def main(args):
    threads = []

    for arg in args:
        thread = threading.Thread(target=worker, args=(arg,))
        threads.append(thread)
        thread.start()

    # Register a hotkey for Shift + Q to exit the program
    keyboard.add_hotkey('Shift + q', signal_handler)

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == '-f':
            if len(sys.argv) < 3:
                print("Usage: python __init__.py -f <filename>")
                sys.exit(1)
            filename = sys.argv[2]
            with open(filename, 'r') as file:
                args = file.read().split()
            main(args)
        else:
            args = sys.argv[1:]
            main(args)
    else:
        print("Usage: python __init__.py <arg1> <arg2> ...")

