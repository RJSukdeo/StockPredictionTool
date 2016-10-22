import logging
import os


# Class that is responsible for logging any errors or warnings that occur while running the tool..... logs to log.log
# which is found in the same folder as the code.
class Logger:

    def __init__(self, logFileName):
        self.createLogFile(logFileName)
        logging.basicConfig(filename=logFileName, level=logging.WARNING)

    def createLogFile(self, logFileName):
        if os.path.isfile(os.curdir+"/"+logFileName):
            os.remove(os.curdir+"/"+logFileName)

        self.logFile = open(logFileName, 'w')

    def closeLogFile(self):
        self.logFile.close()

