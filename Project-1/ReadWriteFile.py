# *****    Write data into file   *********** 
from pathlib import Path
#print(Path.home())
loc= Path('C:/DATA/RK/Python/Project-1/RAKA1/MyData.txt')
file_content='''
 Hi All,
 
 This is Rakesh and writing you a test email.
 
 Adding new test line. 123456
 
 Thanks,
 Rakesh.  
'''

testFile=open(loc,'w',encoding='UTF-8')
testFile.write(file_content)
#data=testFile.read()
testFile.close()

data=testFile.read()
print(data)



# # *****    Read whole file   *********** 
# from pathlib import Path
# #print(Path.home())
# loc= Path('C:/DATA/RK/Python/Project-1/RAKA1/MyData.txt')

# file_data=open(loc,encoding='UTF-8')
# data=file_data.read()
# print(data)




# # *****    Read lines from file   *********** 
# from pathlib import Path
# #print(Path.home())
# loc= Path('C:/DATA/RK/Python/Project-1/RAKA1/MyData.txt')

# file_data=open(loc,encoding='UTF-8')
# data=file_data.readlines()
# print(data)