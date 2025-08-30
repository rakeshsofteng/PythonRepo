
# #save data to shelve
# import shelve
# shelf_file = shelve.open('mydata')


# shelf_file['users'] = ['Rakesh', 'Mukesh','Pooka', 'Simon', 'Ravi', 'Rohan', 'Suresh']
# shelf_file['dev'] = ['Rakesh', 'Mukesh','Pooka']
# shelf_file['qa'] = ['Simon', 'Ravi', 'Rohan', 'Suresh']
# shelf_file.close()



# read data from shelve
import shelve
shelf_file = shelve.open('mydata')

print(list(shelf_file.keys()))
#shelf_file.clear() # clear all data in shelve
first = True
for key in shelf_file:
    if not first:
        print('*'*80)
    print(f"{key}: {shelf_file[key]}")
    first = False
    
#print(shelf_file['users'])
shelf_file.close()
