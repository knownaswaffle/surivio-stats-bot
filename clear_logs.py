# DANGEROUS: erases all logs

import os

for fname in os.listdir('logs'):
    with open('logs/' + fname, 'w'):
        pass # truncate

    
