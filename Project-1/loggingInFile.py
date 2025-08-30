##
## we will create log file, it will get created in rot folder.
##
import logging
logging.basicConfig(filename='myProgramLog.txt', level=logging.DEBUG,format=' %(asctime)s -  %(levelname)s -  %(message)s')
logging.debug('Start of program')

def factorial(n):
    logging.debug('Start of factorial(' + str(n) + ')')
    total = 1
    for i in range(1,n + 1):
        total *= i
        logging.debug('i is ' + str(i) + ', total is ' + str(total))
    logging.debug('End of factorial(' + str(n) + ')')
    return total


factorial(5)
logging.debug('End of program')
