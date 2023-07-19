# tuple = collection which is ordered and unchangeable(immutable)
#         used to group together related data

student = ("Jay",21,"Female")

print(student.count("Jay"))
print(student.index("Female"))

for x in student:
    print(x)

if "Jay" in student:
    print("Jay is here!")