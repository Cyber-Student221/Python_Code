# keyword arguments = arguments preceded by an identifier when we pass them to a function 
#                     The order of the arguments doesn't matter, unlike positional arguments
#                     Python knows the names of the arguments that our function receives


def hello(first,middle,last):
    print("Hello " + first + " " + middle + " " + last)

# hello("Jay", "Bird", "Code") #positional arguments (position matters) (change positions for a different order)
hello(last="Code", middle="Bird", first="Jay" ) # preceded by the identifier in the function (position does not matter)