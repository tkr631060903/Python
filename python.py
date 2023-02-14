from email.mime import base
import math
import time
import functools
import cv2
import keyboard
import json
from abc import ABCMeta, abstractmethod


class Employee(object):
    def __init__(self,name,salary) -> None:
        self._name =name
        self._salary=salary
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self,name):
        self._name=name

    @abstractmethod
    def get_salary(self):
        return self._salary

    @abstractmethod
    def set_salary(self,salary):
        self._salary=salary

class Manager(Employee):
    def __init__(self, name, salary) -> None:
        super().__init__(name, salary)

    def get_salary(self):
        return super().get_salary()

class Programer(Employee):
    def __init__(self, name, salary,h) -> None:
        super().__init__(name, salary)
        self._h=h


def main():
    ma=Manager("123",15000)
    print(ma.get_salary())
      

# class Person(object):
    
#     def __init__(self, name, age):
#         self._name = name
#         self._age = age

#     # 访问器 - getter方法
#     @property
#     def name(self):
#         return self._name

#     @name.setter
#     def name(self,name):
#         if isinstance(name,str):
#             self._name = name

#     # 访问器 - getter方法
#     @property
#     def age(self):
#         return self._age

#     # 修改器 - setter方法
#     @age.setter
#     def age(self, age):
#         self._age = age

#     def play(self):
#         if self._age <= 16:
#             print('%s正在玩飞行棋.' % self._name)
#         else:
#             print('%s正在玩斗地主.' % self._name)
    
    


# def main():
#     person = Person('王大锤', 12)
#     person.name="2"
#     person.play()
#     person.age = 22
#     person.play()
    # person.name = '白元芳'  # AttributeError: can't set attribute


if __name__ == '__main__':
    main()
# Camera.video_demo()
# cv2.destroyAllWindows()

# print("hello world");
# print(100+2+300);
# print(2**10);
# print('''11
# 22
# 33
# 44 55''')
# print("11","22","33","44","55")
# print("100 + 200 =",100+200)
# # name = input("请输入 ")
# # print("hello",name)

# A = 100
# if A <= 0:
#     print(A)
# else:
#     print(-A)

# print("1024 * 768 =", 1024*768)
# print("i\'m \"ok\"!")
# print(r'''hello,\n
# world''')

# a = 123 # a是整数
# print(a)
# a = 'ABC' # a变为字符串
# print(a)
# x = 10
# x = x + 2
# print(x)

# n = 123
# f = 456.789
# s1 = 'Hello, world'
# s2 = 'Hello, \'Adam\''
# s3 = r'Hello, "Bart"'
# s4 = r'''Hello,
# Lisa!'''
# print(n)
# print(f)
# print(s1)
# print(s2)
# print(s3)
# print(s4)

# a = ord("A")
# print(a)
# a = ord("中")
# print(a)
# a = chr(66)
# print(a)
# a = chr(25991)
# print(a)

# print("Hi, %s, you have $%d." % ('Michael', 1000000))
# print('%2d-%02d' % (3, 1))
# print('%.2f' % 3.1415926)

##########################
# 字符串
##########################
# s1 = 72
# s2 = 85
# print("提升了{1:.1f}%", format(85/72))
# r = (s2-s1)/s1*100
# print('小明提升了:%.2f%%'%r)
# print("{0}提升了{1:.1f}%".format("小明", r))
# print(f"小明提升了{r:.3f}%")
#print('growth rate: %d %%' % 7)

##########################
# 条件判断
##########################
# age = input()
# age = int(age)
# if age >= 18:
#     print("adult", age)
# elif age < 18:
#     print("teenager", age)
# else:
#     print("input error")

# height = input("请输入身高(m):")
# weight = input("请输入体重(kg):")
# height = float(height)
# weight = float(weight)
# BMI = weight/(height**2)
# if BMI < 18.5:
#     print("过轻")
# elif 18.5 <= BMI < 25:
#     print("正常")
# elif 25 <= BMI < 28:
#     print("过重")
# elif 28 <= BMI < 32:
#     print("肥胖")
# elif BMI >= 32:
#     print("严重肥胖")
# else:
#     print("竹竿")

# height = input("请输入身高(m):")
# weight = input("请输入体重(kg):")
# height = float(height)
# weight = float(weight)
# BMI = weight/(height**2)
# if BMI < 18.5:
#     print("过轻")
# elif BMI < 25:
#     print("正常")
# elif BMI < 28:
#     print("过重")
# elif BMI < 32:
#     print("肥胖")
# else:
#     print("严重肥胖")

##########################
# 循环
##########################
# list = [1, 2, 3]
# for lists in list:
#     print(lists)

# sum = 0
# for x in [1, 2, 3, 4, 5]:
#     sum = sum + x
# print(sum)

# list = (range(100))
# print(list)

# sum = 0
# for x in range(101):
#     sum = sum + x
# print(sum)

# sum = 0
# n = 99
# while n > 0:
#     sum = sum + n
#     n = n - 2
# print(sum)

# L = ['Bart', 'Lisa', 'Adam']
# for x in L:
#     print(x)

# n = 0
# while n < len(L):
#     print(L[n])
#     n = n + 1

##########################
# 使用dict和set
##########################
# d = {'Michael': 95, 'Bob': 75, 'Tracy': 85}
# print(d['Michael'])
# print(d['Bob'])
# d['Bob'] = 60
# print(d['Bob'])
# print('Tracy' in d)
# print('sekiro' in d)
# if 'sekiro' in d:
#     print('sekiro' in d)
# else:
#     d.get('sekiro')
#     d['sekiro'] = 100
#     print(d['sekiro'])
# print(d)
# d.pop("sekiro")
# print(d)

# s = set([1, 2, 3])
# print(s)
# c = set([1, 1, 2, 2, 3, 3])
# print(c)
# s.add(4)
# print(s)
# s.add(4)
# print(s)
# s.remove(4)
# print(s)

# s1 = set([1, 2, 3])
# s2 = set([2, 3, 4])
# print(s1 & s2)
# print(s1 | s2)

# ##########################
# ##删除重复字符
# ##########################
# s=("X2HIL-V1_0_0",
# "M4",
# "C1",
# "C1",
# "C1",
# "C1",
# "M4C",
# "M4C",
# "M4C",
# "F1",
# )
# m=[]
# for i in s:
#     if i  not in m:
#         m.append(i)
# m.sort(key=str,reverse=False)
# print(' , '.join(m))

# def move(x, y, step, angle=0):
#     nx = x + step * math.cos(angle)
#     ny = y - step * math.sin(angle)
#     return nx, ny

# x, y = move(100, 100, 60, math.pi / 6)
# print(x, y)

# r = move(100, 100, 60, math.pi / 6)
# print(r)

# def quadratic(a, b, c):
#     a = float(a)
#     b = float(b)
#     c = float(c)
#     if not isinstance(a,(int, float)):
#         # raise TypeError('bad operand type')
#         print("a输入数值类型错误")
#     elif b ** 2 - 4 * a * c < 0:
#         print("该方程无解")
#     elif not isinstance(a,(int, float)):
#         print("b输入数值类型错误")
#     elif not isinstance(a,(int, float)):
#         print("b输入数值类型错误")
#     else:
#         x1 = (-b + math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
#         x2 = (-b - math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
#         print(x1, x2)
#         return x1, x2

# print('quadratic(2, 3, 1) =', quadratic(2, 3, 1))
# print('quadratic(1, 3, -4) =', quadratic(1, 3, -4))

# if quadratic(2, 3, 1) != (-0.5, -1.0):
#     print('测试失败')
# elif quadratic(1, 3, -4) != (1.0, -4.0):
#     print('测试失败')
# else:
#     print('测试成功')

# x1, x2 = quadratic(2, 3, 1)
# print(x1, x2)
# a = input("请输入a的值：")
# b = input("请输入b的值：")
# c = input("请输入c的值：")
# quadratic(a, b, c)

# def power(x):
#     return x * x
# print(power(3))

# def power1(x, n):
#     s = 1
#     while n > 0:
#         n = n - 1
#         s = s * x
#     return s
# print(power1(2, 3))

# # n = 2为power1的默认参数
# def power1(x, n = 2):
#     s = 1
#     while n > 0:
#         n = n - 1
#         s = s * x
#     return s
# print(power1(2))

# def calc(numbers):
#     sum = 0
#     for n in numbers:
#         sum = sum + n * n
#     return sum

# print(calc([1, 2, 3]))
# print(calc((1, 3, 5, 7)))

# def calc1(*numbers):
#     sum = 0
#     for n in numbers:
#         sum = sum + n * n
#     return sum

# print(calc1(1, 2, 3))
# print(calc1())

# nums = [1, 2, 3]
# print(calc1(nums[0], nums[1], nums[2]))

# ##########################
# ##函数参数
# ##########################
# def mul(*numbers):
#     if not numbers:
#         raise TypeError ('不能为空')
#     sum = 1
#     for n in numbers:
#         sum = sum * n
#     if not isinstance(sum, (int, float)):
#         raise TypeError("请输入数值")
#     return sum

# # print(type(mul(5)))
# # print(mul("g, f, f"))
# # mul("g, f, f")
# # print(type(mul(5, 6, 7, 9)))

# print('mul(5) =', mul(5))
# print('mul(5, 6) =', mul(5, 6))
# print('mul(5, 6, 7) =', mul(5, 6, 7))
# print('mul(5, 6, 7, 9) =', mul(5, 6, 7, 9))
# if mul(5) != 5:
#     print('测试失败!')
# elif mul(5, 6) != 30:
#     print('测试失败!')
# elif mul(5, 6, 7) != 210:
#     print('测试失败!')
# elif mul(5, 6, 7, 9) != 1890:
#     print('测试失败!')
# else:
#     try:
#         mul()
#         print('测试失败!')
#     except TypeError:
#         print('测试成功!')

# ##########################
# ##递归函数
# ##########################

# def fact(n):
#     if n==1:
#         return 1
#     return n * fact(n - 1)

# print(fact(5))

# 汉诺塔
# def hanoi(n, a, b, c):
#     if n == 1:
#         print(a, '-->', c)
#     else:
#         hanoi(n - 1, a, c, b)
#         print(a, '-->', c)
#         hanoi(n - 1, b, a, c)
# # 调用
# hanoi(3, 'A', 'B', 'C')

# def lists(args):
#     n = 1
#     l = []
#     while n <= args:
#         l.append(n)
#         n += 2
#     print(l)
# lists(100)

# class1 = ['w', "2", "3", "sekiro", "to", "okami"]
# print(class1)
# print(len(class1))
# print(class1[1])
# # for name in class1:
# #     print(name)
# class1.append("ino")
# print(len(class1))
# p = ['asp', 'php']
# s = ['python', 'java', p, 'scheme']
# print(len(p))
# print(len(s))
# print(s[2][1])
# for name in s:
#     print(name)
# q = (1, 2, 3)
# print(len(q))

# # -*- coding: utf-8 -*-

# L = [
#     ['Apple', 'Google', 'Microsoft'],
#     ['Java', 'Python', 'Ruby', 'PHP'],
#     ['Adam', 'Bart', 'Lisa']
# ]
# print(L[0][0])
# print(L[1][1])
# print(L[2][2])

# print(abs(-100))
# print(abs(100))
# print(abs(-1.2))
# print(max(1, 2, 3, 9, -10, abs(-20)))
# print(int("12344"))
# print(int(12344))
# print(str(12344))
# print(float("1.23"))

# print(hex(255))
# print(hex(1000))

# def my_abs(x):
#     if x >= 0:
#         return x
#     else:
#         return -x
# n = input()
# n = float(n)
# print(my_abs(n))

# def my_abs1(x):
#     if not isinstance(x, (int, float)):
#         raise TypeError ("类型错误")
#     if x >= 0:
#         return x
#     else:
#         return -x
# print(my_abs1(2))

# def move(x, y, step, angle = 0):
#     nx = x + step * math.cos(angle)
#     ny = y + step * math.sin(angle)
#     return nx, ny

# ##########################
# ##切片
# ##########################

# l = list(range(100))

# print(l[:10])   # 取顺数前十个数
# print(l[-10:])  # 取倒数十个数
# print(l[20:30]) # 取第20~30的数
# print(l[::5])   # 所有数，每5个取一个

# 去除字符串首尾的空格

# def trim(args):
#     s = 0
#     m = 0
#     x = 0
#     for n in args:
#         x += 1
#     for n in args:
#         if n != " ":
#             s = s
#             break
#         elif n == " ":
#             s += 1
#     for n in args[ : : -1]:
#         if n != " ":
#             m = m
#             break
#         elif n == " ":
#             m += 1
#     # print(args[s : x - m])
#     return(args[s:x - m])

# 例子
# def trim(str):
#     if len(str)==0:
#        return str
#     elif str[0] == ' ':
#        str = str[1:]
#        return trim(str)
#     elif str[-1]== ' ':
#        str = str[:-1]
#        return trim(str)
#     else:
#        return str

# # 测试:
# if trim('hello  ') != 'hello':
#     print('测试失败!')
# elif trim('  hello') != 'hello':
#     print('测试失败!')
# elif trim('  hello  ') != 'hello':
#     print('测试失败!')
# elif trim('  hello  world  ') != 'hello  world':
#     print('测试失败!')
# elif trim('') != '':
#     print('测试失败!')
# elif trim('    ') != '':
#     print('测试失败!')
# else:
#     print('测试成功!')

##########################
# 迭代
##########################

# 请使用迭代查找一个list中最小和最大值，并返回一个tuple：

# def findMinAndMax(L):
#     i = 0
#     if len(L) == 0:
#         return (None, None)
#     for n in L:
#         if i == 0:
#             max = L[0]
#             min = L[0]
#         elif max < L[i]:
#             max = L[i]
#         elif min > L[i]:
#             min = L[i]
#         i += 1
#     return(min,max)

# 例子
# def findMinAndMax(L):
#     if len(L) == 0:
#         return (None, None)
#     else:
#         max = L[0]
#         min = L[0]
#         for n in L:
#             if n > max:
#                 max = n
#             elif n < min:
#                 min = n
#         return (min, max)

# # 测试
# if findMinAndMax([]) != (None, None):
#     print('测试失败!')
# elif findMinAndMax([7]) != (7, 7):
#     print('测试失败!')
# elif findMinAndMax([7, 1]) != (1, 7):
#     print('测试失败!')
# elif findMinAndMax([7, 1, 3, 9, 5]) != (1, 9):
#     print('测试失败!')
# else:
#     print('测试成功!')

# ##########################
# ## 列表生成式
# ##########################

# L = []
# for x in range(1, 11):
#     L.append(x * x)
# print(L)

# # 写列表生成式时，把要生成的元素x * x放到前面，后面跟for循环，就可以把list创建出来，十分有用，多写几次，很快就可以熟悉这种语法。
# l = [x * x for x in range(1, 11)]
# print(l)

# # for循环后面还可以加上if判断，这样我们就可以筛选出仅偶数的平方：
# l = [x * x for x in range(1, 11) if x % 2 == 0]
# print(l)

# # 可以使用两层循环，可以生成全排列：
# L = [m + n for m in 'abc' for n in 'xyz']
# print(L)

# # for循环其实可以同时使用两个甚至多个变量，比如dict的items()可以同时迭代key和value：
# d = {'x': 'a', 'y': 'b', 'z': 'c'}
# for k, v in d.items():
#     print(k, '=', v)

# # 列表生成式也可以使用两个变量来生成list
# d = {'x': 'a', 'y': 'b', 'z': 'c'}
# d1 = [k + '=' + v for k, v in d.items()]
# print(d)
# print(d1)

# # 把一个list中所有的字符串变成小写
# l = ['Hello', 'World', 'IBM', 'Apple']
# l1 = [s.lower() for s in l]
# print(l1)

# # 把if写在for前面必须加else，否则报错这是因为for前面的部分是一个表达式，它必须根据x计算出一个结果。
# # 因此，考察表达式：x if x % 2 == 0，它无法根据x计算出结果，因为缺少else，必须加上else
# l = [x if x % 2 == 0 else -x for x in range(1, 11)]
# print(l)
# # 上述for前面的表达式x if x % 2 == 0 else -x才能根据x计算出确定的结果。
# # 可见，在一个列表生成式中，for前面的if ... else是表达式，而for后面的if是过滤条件，不能带else。

# ### 请修改列表生成式，通过添加if语句保证列表生成式能正确地执行,并将既包含字符串又包含整数的list中字符串转换成小写
# L1 = ['Hello', 'World', 18, 'Apple', None]
# L2 = [x.lower() for x in L1 if isinstance(x,str) == True]

# # 测试:
# print(L2)
# if L2 == ['hello', 'world', 'apple']:
#     print('测试通过!')
# else:
#     print('测试失败!')

##########################
# 生成器(generator)
##########################

# 只要把一个列表生成式的[]改成()，就创建了一个generator：
# l = [x*x for x in range(1,11)]  #list
# print(l)

# 创建L和g的区别仅在于最外层的[]和()，L是一个list，而g是一个generator。
# g = (x*x for x in range(1,11))  #generator
# print(g)
# for x in g:
#     print(x)

# def fib(max):  #生成斐波拉契数列，list
#     n, a, b = 0, 0, 1
#     while n < max:
#         print(b)
#         a, b = b, a + b
#         n = n + 1
#     return 'done'

# print(fib(6))

# 如果一个函数定义中包含yield关键字，那么这个函数就不再是一个普通函数，而是一个generator函数，调用一个generator函数将返回一个generator：
# def fib(max):  #生成斐波拉契数列，generator
#     n, a, b = 0, 0, 1
#     while n < max:
#         yield b
#         a, b = b, a + b
#         n = n + 1
#     return 'done'
# print(fib(6))
# for x in fib(6):
#     print(x)

# 练习生成generator 杨辉三角
# 例子
# def triangles():
#     L = [1]
#     while True:
#         yield L
#         L = [sum(i) for i in zip([0]+L, L+[0])]

# n = 0
# results = []
# for t in triangles():
#     results.append(t)
#     n = n + 1
#     if n == 10:
#         break

# for t in results:
#     print(t)

# if results == [
#     [1],
#     [1, 1],
#     [1, 2, 1],
#     [1, 3, 3, 1],
#     [1, 4, 6, 4, 1],
#     [1, 5, 10, 10, 5, 1],
#     [1, 6, 15, 20, 15, 6, 1],
#     [1, 7, 21, 35, 35, 21, 7, 1],
#     [1, 8, 28, 56, 70, 56, 28, 8, 1],
#     [1, 9, 36, 84, 126, 126, 84, 36, 9, 1]
# ]:
#     print('测试通过!')
# else:
#     print('测试失败!')

# ##########################
# ## 高阶函数
# ##########################

# def add(x, y, f):
#     return f(x) + f(y)

# print(add(-5, 6, abs))

##########################
# map/reduce
##########################

# def f(x):
#     return x * x

# r = map(f, [1, 2, 3, 4, 5, 6, 7, 8, 9])
# print(list(r))
# # print(tuple(r))

# print(list(map(str, [1, 2, 3, 4, 5, 6, 7, 8, 9])))

# def add(x, y):
#     return x + y

# print(reduce(add, [1, 3, 5, 7, 9]))

##########################
# list改成首字母大写，其他小写的规范名字
##########################

# def normalize(str):
#     str = str[0].upper() + str[1:].lower()
#     return str

# L1 = ['adam', 'LISA', 'barT']

# # 测试:
# L1 = ['adam', 'LISA', 'barT']
# L2 = list(map(normalize, L1))
# print(L2)

# def prod(L):
#     def sum(x,y):
#         return x*y
#     L=reduce(sum,L)
#     return L

# print('3 * 5 * 7 * 9 =', prod([3, 5, 7, 9]))
# if prod([3, 5, 7, 9]) == 945:
#     print('测试成功!')
# else:
#     print('测试失败!')

# def str2float(s):
#     return float(s)

# print('str2float(\'123.456\') =', str2float('123.456'))
# if abs(str2float('123.456') - 123.456) < 0.00001:
#     print('测试成功!')
# else:
#     print('测试失败!')

# def is_odd(n):
#     return n % 2 == 1

# print(list(map(is_odd, [1, 2, 4, 5, 6, 9, 10, 15])))
# print(list(filter(is_odd, [1, 2, 4, 5, 6, 9, 10, 15])))

# def not_empty(s):
#     return s and s.strip()

# print(list(map(not_empty, ['A', '', 'B', None, 'C', '  '])))
# print(list(filter(not_empty, ['A', '', 'B', None, 'C', '  '])))

##########################
# filter
##########################

# def is_palindrome(n):
#     x = str(n)
#     if x[0] == x[-1:]:
#         return True

# # 测试:
# output = filter(is_palindrome, range(1, 1000))
# print('1~1000:', list(output))
# if list(filter(is_palindrome, range(1, 200))) == [
#         1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22, 33, 44, 55, 66, 77, 88, 99, 101,
#         111, 121, 131, 141, 151, 161, 171, 181, 191
# ]:
#     print('测试成功!')
# else:
#     print('测试失败!')

##########################
# sorted
##########################

# # print(sorted([36, 5, -12, 9, -21]))

# # print(sorted([36, 5, -12, 9, -21], key = abs))

# L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]

# def by_name(t):
#     return t[0]

# def by_score(t):
#     return t[1]

# L2 = sorted(L, key=by_name)
# print(L2)

# L2 = sorted(L, key=by_score, reverse=True)
# print(L2)

##########################
# 返回函数
##########################

# def lazy_sum(*args):
#     def sum():
#         ax = 0
#         for n in args:
#             ax += n
#         return ax
#     return sum

# f = lazy_sum(1, 3, 5, 7, 9)
# print(f)
# print(f())

# def count():
#     fs = []
#     for i in range(1, 4):
#         def f():
#              return i*i
#         fs.append(f)
#     return fs

# f1, f2, f3 = count()

# print(f1(),f2(),f3())

# def inc():
#     x = 0
#     def fn():
#         # 仅读取x的值:
#         return x + 1
#     return fn
# f = inc()
# print(f()) # 1

# def inc():
#     x = 0

#     def fn():
#         nonlocal x
#         x = x+1
#         return x
#     return fn

# f = inc()
# print(f())  # 1

# def createCounter():
#     x = 0

#     def counter():
#         nonlocal x
#         x = x+1
#         return x
#     return counter

# counterA = createCounter()
# print(counterA(), counterA(), counterA(), counterA(), counterA())  # 1 2 3 4 5
# counterB = createCounter()
# if [counterB(), counterB(), counterB(), counterB()] == [1, 2, 3, 4]:
#     print('测试通过!')
# else:
#     print('测试失败!')

##########################
# 匿名函数(lambda)
##########################

# def is_odd(n):
#     return n % 2 == 1

# L = list(filter(is_odd, range(1, 20)))
# print(L)
# L = list(filter(lambda x: x % 2 == 1, range(1, 20)))
# print(L)

############################
# 装饰器(Decorator)
############################

# def outer(origin):  # 当func1函数调用时origin -> func1
#     def inner(*args, **kwargs): # 传任意个参数
#         print("before")
#         res = origin(*args, **kwargs)  # 调用原来的func1()函数
#         print("after")
#         return res
#     return inner

# @outer  # func1 = outer(func1)
# def func1(a1):
#     print("fun1")
#     value = (1, 2, 3)
#     return value

# @outer  # func2 = outer(func2)
# def func2(a1, a2):
#     print("func2")
#     value = (4, 5, 6)
#     return value

# @outer  # func3 = outer(func3)
# def func3(a3):
#     print("func3")
#     value = (7, 8, 9)
#     return value

# func1(1)
# func2(1, 2)
# func3(333)

# 习题
# def metric(func):
#     def wrapper(*args):
#         t1 = time.time()
#         result = func(*args)
#         t2 = time.time()
#         print("Total time: {:.4} s".format(t2 - t1))
#         return result
#     return wrapper

# # 测试
# @metric
# def fast(x, y):
#     time.sleep(0.0012)
#     return x + y

# @metric
# def slow(x, y, z):
#     time.sleep(0.1234)
#     return x * y * z

# f = fast(11, 22)
# s = slow(11, 22, 33)
# if f != 33:
#     print('测试失败!')
# elif s != 7986:
#     print('测试失败!')

############################
# 偏函数(Partial function)
############################

# int2 = functools.partial(int, base=2)
# print(int2("100"))
# print(int2("100", base=10))
# print(int2("100",base=16))

# def add(*args):
#     return sum(args)

# add_100 = functools.partial(add, 100)
# print(add_100(1, 2, 3))
# print("-" * 20)
# add_101 = functools.partial(add, 101)
# print(add_101(1, 2, 3))


############################
# json数据解析
############################

# data = {"no": 1, "name": "lia", "url": "www"}
# data1=0

# with open("data.json", "w") as f:
#     json.dump(data, f)

# with open("data.json", "r") as f:
#     data1 = json.load(f)

# print(data1)

############################
# 类(Class)
############################

# class Student(object):

#     def __init__(self, name, score):
#         self.name = name
#         self.score = score

#     def print_score(self):
#         print("%s:%s" % (self.name, self.score))

#     def get_grade(self):
#         if self.score >= 90:
#             return 'A'
#         elif self.score >= 60:
#             return 'B'
#         else:
#             return 'C'

# bart = Student("Bart Simpson", 60)
# print(bart)
# print(bart.name)
# print(bart.score)
# print(bart.print_score())

# lisa = Student('Lisa', 99)
# bart = Student('Bart', 59)
# print(lisa.name, lisa.get_grade())
# print(bart.name, bart.get_grade())
