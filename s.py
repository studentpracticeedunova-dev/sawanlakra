# import sys
# a=152555445312
# print(sys.getrefcount(a))
#
# a=18
# print(sys.getrefcount(a))
#
# a=20
# print(sys.getrefcount(a))
#
# a="hello"
# print(sys.getrefcount(a))
#
# a=[1,2,3]
# b=[4,5,6]
# print(sys.getrefcount(a))
# print(sys.getrefcount(b))
# a.append(b)
# b.append(a)
# print(a)
# print(b)

# import gc
#
# a = [1, 2, 3,4,5,6]
# # b = [4,5,6]
#
# # a=10
# c=gc.collect()
#
# print("Garbage collected =",c)

import gc

print(gc.get_threshold())

print(gc.get_count())

gc.collect()

