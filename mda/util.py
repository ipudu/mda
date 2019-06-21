import os
import time
import textwrap

width = 80

def timeit(method):
    """Output the time a function takes to execute

    Arguments:
        method {function} -- function called

    Returns:
        string -- time
    """
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' % \
                (method.__name__, (te - ts) * 1000))
        return result
    return timed

def output_welcome():
    
    #............................................................................
    logo = """
                                            88            
                                            88            
                                            88            
                88,dPYba,,adPYba,    ,adPPYb,88  ,adPPYYba,
                88P'   "88"    "8a  a8"    `Y88  ""     `Y8
                88      88      88  8b       88  ,adPPPPP88
                88      88      88  "8a,   ,d88  88,    ,88
                88      88      88   `"8bbdP"Y8  `"8bbdP"Y8
                
                   mda: analysis tools for MD simulations
            """
    
    logo += '\n' + '.' * width
    print(logo)

def output_end():
    art = '\n' + '.' * width
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
    output_end()