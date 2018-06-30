from sys import argv
from console_interface import ConsoleInterface
from console_renderer import renderBoard


def main():
    arguments = argv[1:]
    
    ## TODO: initialize the interface
    interface = ConsoleInterface(arguments, renderBoard)
    interface.start()

    # game is over



if __name__ == "__main__":
    main()