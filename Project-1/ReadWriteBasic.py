from pathlib import Path

loc= Path('C:/DATA/RK/Python/Project-1/RAKA1/MyData.txt')

print("Simple exists="+ str(loc.exists()))     # If path exist then go ahead with writing. 
print("File exists="+ str(loc.is_file()))
print("Dir exists="+ str(loc.is_dir()))


data='''
 Hi All,
 
 This is Rakesh and writing you a test email.
 
 Thanks & regards,
 Rakesh.  
'''

#loc.write_text(data)
#print(loc.read_text())

