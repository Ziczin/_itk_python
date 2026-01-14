s = "Hello"
try:
    s[0] = "h"
    print(s)
    print("Correct!")
except Exception as e:
    print(e)
