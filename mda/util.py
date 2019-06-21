import os
import textwrap

width = 80

def output_welcome():
    logo = textwrap.dedent("""
                                                          88            
                                                          88            
                                                          88            
                              88,dPYba,,adPYba,    ,adPPYb,88  ,adPPYYba,
                              88P'   "88"    "8a  a8"    `Y88  ""     `Y8
                              88      88      88  8b       88  ,adPPPPP88
                              88      88      88  "8a,   ,d88  88,    ,88
                              88      88      88   `"8bbdP"Y8  `"8bbdP"Y8
                              
                              mda: analysis tools for MD simulations
                           """)
    
    logo += '.' * width

    print(logo)

def output_end():
    art = '.' * width
    art +=  """
                           .
                          ":"
                        ___:____     |"\/"|
                      ,'        `.    \  /
                      |  O        \___/  |
                    ~^~^~^~^~^~^~^~^~^~^~^~^~
            """

    print(art)

    from shutil import which
    # FIXME: the stdout will go to the top of log file
    if which('fortune'):
        os.system('fortune')

if __name__ == '__main__':
    output_welcome()