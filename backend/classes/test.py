#! /bin/python3

from pieces import Vector

ls = list()
for i in (-1, 0, 1):
    for j in (-1, 0,  1):
        if abs(i) != abs(j):
            ls.append(Vector((i, j)))
print(ls)
print(len(ls))

print(Vector((0, 1)) + Vector((1, 2)))

