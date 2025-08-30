from pathlib import Path
import shutil
import os

h = Path(r"C:\DATA\RK\Python\testFiles")
print(h)
#shutil.copytree(h, h.parent / "testFilesCopy", dirs_exist_ok=True)

#shutil.copy(h / "accounts.txt",  h.parent / "testFilesCopy" / "accountsRaka.txt")

#shutil.move(h / "accounts.txt",  h.parent / "testFilesCopy" / "accountsRaka1.txt")

loc= h.parent / "testFilesCopy" / "test1"
print(loc)

#os.unlink( loc /"file1.txt")
os.rmdir( loc)
print("done")





