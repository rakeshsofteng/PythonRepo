from pathlib import Path
import os
my_files = ['accounts.txt', 'details.csv', 'invite.docx']

#for filename in my_files:
#    print(Path(r'C:\DATA\RK\Python\testFiles', filename))

p=Path.cwd()
print(p)  

#loc= str(Path.cwd())+'\RAKA1'
#print(loc)
#os.makedirs(loc) 

#data=list(p.glob('*'))
#print(data[0:3])

loc= Path(str(Path.cwd())+'\RAKA1')
print(loc.exists())