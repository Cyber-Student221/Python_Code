# set = collection which is unordered, unindexed. NO dupilacte values
# set is faster than a list when checking if something is within a set
utensils = {"fork", "spoon", "knife"}
dishes = {"bowl", "plate", "cup", "knife"}

# utensils.add("napkin")
# utensils.remove("fork")
# utensils.clear()
# utensils.update(dishes)

print(utensils.difference(dishes))
print(dishes.difference(utensils))
print(utensils.intersection(dishes))

# dinner_table = utensils.union(dishes)

# for x in dinner_table:
#     print(x)

