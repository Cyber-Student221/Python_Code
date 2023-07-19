# dictionary = changeable, unordered collection of unique key:value pairs (mutable - can be change after program is run)
#              Fast because they use hashing, allowing us to access a value quickly

capitals = {'USA': 'Washington DC', 
            'India': 'New Delhi',
            'China': 'Beijing',
            'Russia': 'Moscow'}

# print(capitals['Russia']) # Not always safe to call values like this (keyError when the key value not in the dict)
# print(capitals['Germany'])

# print(capitals.get('Germany')) # Safer way as it returns none if the key is not in dict

# print(capitals.keys())
# print(capitals.values())
# print(capitals.items())

capitals.update({'Germany': 'Berlin'})
capitals.update({'USA': 'Las Vegas'})

capitals.pop('China')
capitals.clear()

for key, value in capitals.items():
    print(key, value)