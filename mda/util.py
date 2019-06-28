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
                                                                    
                88888888ba,    88b           d88         db         
                88      `"8b   888b         d888        d88b        
                88        `8b  88`8b       d8'88       d8'`8b       
                88         88  88 `8b     d8' 88      d8'  `8b      
                88         88  88  `8b   d8'  88     d8YaaaaY8b     
                88         8P  88   `8b d8'   88    d8''''''''8b    
                88      .a8P   88    `888'    88   d8'        `8b   
                88888888Y"'    88     `8'     88  d8'          `8b  
                                                                
                     MDA: Analysis Tools for MD Simulations
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