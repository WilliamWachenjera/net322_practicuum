import threading
import time

def say_hello():

    print(f"Hello! | {time.strftime("%H:%M:%S")}")
    time.sleep(3)
    print(f"Hello again! | {time.strftime("%H:%M:%S")}")

def say_goodbye():
    print(f"Goodbye! | {time.strftime("%H:%M:%S")}")
    time.sleep(2)
    print(f"Goodbye again! | {time.strftime("%H:%M:%S")}")

def main():
    # Run tasks sequentially
    say_hello() 
    say_goodbye()

if __name__ == "__main__":
    main()