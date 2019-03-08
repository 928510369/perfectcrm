from django.test import TestCase

# Create your tests here.
# class TestA(object):
#     def __new__(cls, *args, **kwargs):
#         print(TestA)
#         return "a"
#
# class TestB(TestA):
#     # def __new__(cls, *args, **kwargs):
#     #     print(TestA)
#     #     return TestA.__new__(cls)
#     pass
#
# a=TestB()
# print(a,type(a))
a={"1":"root","2":"agou"}
def printaa(**b):
    print(b)
printaa(a)
