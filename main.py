import os

for dirpath, dirnames, files in os.walk('.'):
    #print(f'Found directory: {dirpath}')
    for file_name in files:
        if file_name == 'bioreactor.py':
          print("Running " + file_name) 
          exec(open(dirpath + '/' + file_name).read())