import sys
import os



def main():
    for entry in os.scandir(sys.argv[1]):
        print(f"found entry! {entry}")



if __name__ == "__main__":
    main()