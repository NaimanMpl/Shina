import datetime
import math

curr_time = datetime.datetime.now()
print(curr_time.strftime('%Y-%m-%d %H:%M:%S'))
print(type(curr_time.minute))

curr_xp = 0
curr_lvl = 0
niveau = (math.sqrt(100 * (2 * curr_xp + 25)) + 50) / 100
xp = (curr_lvl**2 + curr_lvl) / 2 * 100 - (curr_lvl * 100)
print(xp, niveau)

for i in range(1, 10001):
    curr_xp += 10
    niveau = (math.sqrt(100 * (2 * curr_xp + 25)) + 50) / 100
    xp = (niveau**2 + niveau) / 2 * 100 - (niveau * 100)
    print(f"En {i} minutes tu es niveau {niveau} et tu as besoin de {xp} d'expérience")

def u(n):
    if n == 1:
        return 7
    else:
        return u(n-1) + 0.9

