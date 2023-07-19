# function = a block of code which is exedcuted only when it is called (used for collating repeating code)

def hello(first_name, last_name, age):
    print('Hello ' + first_name + ' ' + last_name)
    print('You are ' + str(age) + " years old")
    print('Have a nice day!')

# my_name = 'BoB'
# hello(my_name)
# hello('Jay') #func call
# hello('Bird')
hello('Jay', 'Bird', 21)