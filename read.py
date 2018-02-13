#ALDY 13 FEBRUARY 2018
import glob
import os
import time
import subprocess

files = os.listdir('D:\lamjaya')
list_of_files = glob.glob('D:\lamjaya\*.txt') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)
#os.listdir(list_of_files)

def refresh():
     dire = ('D:\lamjaya')
     g = os.listdir(dire)
     print(g)
def read() :
     g = open(latest_file,'rb')
     f = g.readlines()
     print ('')
     print(latest_file)
     print('PLATE NUMBER = ',(f[4]))
     print ('LOCATION = ', (f[9]))
     print ('LOCAL TIME = ',(f[14]))
     time.sleep(0.5)
     
def delete():
     os.unlink(latest_file)

def upload
     
read()
refresh()
delete()
