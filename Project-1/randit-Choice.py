# import random
# pets = ['Dog', 'Cat', 'Moose', 'cow','bull']
# r=random.randint(0,4)
# print(r)
# print(pets[r]) 


# choose_data= random.choice(pets)
# print('*'*10)
# print(pets)
# print(choose_data)





# import random
# people = ['Alice', 'Bob', 'Carol', 'David']
# #random.shuffle(people)
# people.append("RAKA")
# #people.insert(0,'Mukesh')
# print(people)
# #del people[0]
# people.remove(people[4]);  # it will remove but will accespt string input name
# print(people)






import random

messages = ['It is certain',
    'It is decidedly so',
    'Yes definitely',
    'Reply hazy try again',
    'Ask again later',
    'Concentrate and ask again',
    'My reply is no',
    'Outlook not so good',
    'Very doubtful']

print('Ask a yes or no question:')
input('>')
print(messages[random.randint(0, len(messages) - 1)])
print('*'*20)
print(random.choice(messages))






