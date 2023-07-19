# type casting: convert the data type of a value to another data type
# Permanent: when redifining the variable
# Temporary change: changing an instance of the variable
# Scenario: you woud change an int/float to a string when concatening strings in a print statement
x = 1   # int
y = 2.0 # float
z = "3" # str

y = int(y)

print("x is " + str(x))
print("y is " +str(y))
print(z*3) # 333 when string