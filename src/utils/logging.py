import logging
from typing import Any
import sys


def getAllLoggers(include_root: bool=False) -> list[str]:
    '''get all loggers chained to root logger at current 

    Args:
      - include_root(bool): True if including root logger otherwise False.

    Returns:
      list[str]: logger names observed at current
    '''

    loggers: list[str] = [] if not include_root else [None,]
    loggers += sorted(logging.root.manager.loggerDict, key=str.lower)  # append all loggers at current
    return loggers


def dumpLoggers(loggers: list[str]=None, fp=sys.stderr):
    '''dump loggers.

    Args:
      - loggers(list[str]): logger names to dump
      - fp: dest of file for print
    '''

    if not loggers:
        loggers = getAllLoggers(True)

    for name in loggers:
        logger = logging.getLogger(name)
        print(f'{logger=}  disabled:{logger.disabled} filter:{logger.filters} handlers:{logger.handlers}', file=fp)


def mkLoggingHandler(handler: type[logging.Handler]|None=None,
              fmt: str='%(asctime)s.%(msecs)03d %(levelname)s [%(name)s]: %(message)s',
              datefmt: str='%Y-%m-%d %H:%M:%S',
              **kwargs: Any) -> logging.Handler:
    '''create Logging Handler instance.
    Args:
      - handler (type): some of logging.Handler
      - fmt (str): format string
      - datefmt (str): date format string
      - **kwargs (Any): parameters to handler constructor

    Returns:
      Handler: instance of logging.Handler.
    '''

    if handler is None:
        h = logging.StreamHandler(stream=sys.stderr)
    else:
        h = handler(**kwargs)
    h.setFormatter( logging.Formatter(fmt=fmt, datefmt=datefmt) )
    return h


def configLogger(logger: logging.Logger|str|None=None,
                 logLevel: str='INFO',
                 handlers: list[logging.Handler]=None) -> logging.Logger:
    '''configure Logger

    Args:
      - logger (logging.Logger|str|None): instance or name of logger to be configured (if None, use RootLogger)
      - logLevel(str): loglevel to assign
      - handlers(list[logging.Handler]): logging handler to attach.

    Returns:
      Logger: instance of Logger. 
    '''

    if isinstance(logger, (str|None)):
        logger = logging.getLogger(logger)

    logger.setLevel(logLevel)

    if handlers in [ None, []]:
        return logger

    #when handlers are specified:

    for c in logger.handlers: # clear current handlers
        logger.removeHandler(c)
    for n in handlers:        # apply handlerss
        n.setLevel(logLevel)  #   set loglevel to each handler for sure.
        logger.addHandler(n)
    return logger


"""
#
# Sample Code:
#

# import lots of lib which use logger
import httpx
import logging
from fastmcp import FastMCP, Client
from utils.logging import dumpLoggers, getAllLoggers, mkLoggingHandler, configLogger

dumpLoggers()
handlers = [ mkLoggingHandler(handler=logging.FileHandler, filename='/tmp/z.log') ]
for k in getAllLoggers( include_root=True):
   configLogger(k, logLevel='DEBUG', handlers=handlers)
dumpLoggers()
"""
