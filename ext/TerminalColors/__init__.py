__author__='Dennis Hafemann, https://github.com/dennishafemann/python-TerminalColors'

# Severals
ESCAPE_SEQUENCE="\033[%sm"

# Styles
RESET = 0
BOLD = 1
UNDERLINE = 4
BLINK = 5
REVERSE_VIDEO = 7

# Colors
BLACK = 30
RED = 31
GREEN = 32
YELLOW = 33
BLUE = 34
MAGENTA = 35
CYAN = 36
WHITE = 37

def _createColoredString(*args):
    """
    Internal method, which generates, returns a color-string.
    """
    value=""

    # Walk through parameters/arguments
    for arg in args[0]:
        if type(arg)==int:
            value+=ESCAPE_SEQUENCE % str(arg)
        else:
            value+=arg

    # If args available, append reset
    if value:
        value+=ESCAPE_SEQUENCE % str(RESET)

    return value

def cprint(*args):
    """
    Directly prints out the generated color-string.
    """
    print(_createColoredString(args))

def rcprint(*args):
    """
    Return a generated color-string.
    """
    return _createColoredString(args)

def error(message):
    """
    For printing/outputting simple, small error messages.
    """
    cprint(RED, message)

if __name__=='__main__':
    # Example
    # Prints directly
    cprint('This text is', RED, ' red', RESET, ' and ', RED, BOLD, 'bold', RESET, '.')

    #  Prints via a variable
    colorString=rcprint('This text is', RED, ' red', RESET, ' and ', RED, BOLD, 'bold', RESET, ', returned.')
    print(colorString)

    # Error
    error('This is a simple, small error message.')