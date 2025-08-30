# while True:
#     print('Who are you?')
#     name = input('>')
#     if name != 'Raka':
#       continue
#     while True:
#         print('Hello, Raka! What is the password? (It is a fish.)')
#         password = input('>')
#         if password == 'fish':
#          print('Access granted.')
#          break
#         else:
#           print('Wrong !! PLease enter password again.')
#           password = input('>')
#     break   #is this correct place to break outer loop        
# print('Access granted.All done now')




print('say Hello to loops !')
i = 0
while i < 5:
    print('On this iteration, i is set to ' + str(i))
    i = i + 1
print('Goodbye!')