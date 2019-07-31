import time
import textwrap
import subprocess

from datetime import datetime
from shutil import which

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
        if "log_time" in kw:
            name = kw.get("log_name", method.__name__.upper())
            kw["log_time"][name] = int((te - ts) * 1000)
        else:
            print("%r  %2.2f ms" % (method.__name__, (te - ts) * 1000))
        return result

    return timed


def output_welcome():

    # ............................................................................
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

    logo += "\n" + "." * width + "\n"
    print(logo)

    return time.time()


def output_end(start):
    e = time.time() - start
    print(
        "\nTotal elapsed time: {} days {} hours {} minutes {:.1f} seconds".format(
            *time_convert(e)
        )
    )

    now = datetime.now()
    date_time = now.strftime("%a %b %d %H:%M:%S %Y.")
    print("Normal termination of MDA at", date_time)

    art = "\n" + "." * width
    art += """
                                .
                                ":"
                              ___:____     |"\/"|
                            ,'        `.    \  /
                            |  O        \___/  |
                          ~^~^~^~^~^~^~^~^~^~^~^~^~
            """

    print(art)

    if which("fortune"):
        fortune = subprocess.check_output("fortune", shell=True)
        print(str(fortune, "utf-8"))


def time_convert(time):
    day = time // (24 * 3600)
    time = time % (24 * 3600)
    hour = time // 3600
    time %= 3600
    minutes = time // 60
    time %= 60
    seconds = time
    return int(day), int(hour), int(minutes), seconds
