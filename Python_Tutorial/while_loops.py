# while loop = a statemnent that will execute its block of code as long as its condition remains true
# always have an escape condition for a loop

# Infinite loop
#while True or 1==1:
#    print("Help! I'm stuck in a loop!")

name = None

while not name:
    name = input("Enter your name: ")

print("Hello " + name)