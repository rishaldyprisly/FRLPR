import glob
import os

list_of_files = glob.glob('D:\camp\htdocs\LPR\*.lpr',) # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)

with open(latest_file) as f:
    f = f.readlines()
#    g = f.readlines(11)
#   h = f.readlines(16)
print ('')
print('PLATE NUMBER = ',(f[5]) )
print ('LOCATION = ', (f[10]))
print ('LOCAL TIME = ',(f[15]) )


