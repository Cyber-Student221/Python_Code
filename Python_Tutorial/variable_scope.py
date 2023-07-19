# scope =   The region that a variable is regocnized
#           A variable is only available from inside the region it is created
#           A global and locally scoped versions of a variable can be created

name = "Jay" # global scope (available inside and outside functions)

def display_name():
    # name = "Bird" # local scope (available only inside this function)
    print(name)


display_name() # prints the local version
print(name) # prints the global version



### show local variable name and print outside to show what local means then compare to global variable
### comment the local name to show the global variable can be accessed in the function
