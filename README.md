# pyxration
Символьная алгебраическая библиотека для создания и описания своих алгебраических систем.

Позволяет создавать свои операции, объекты и алгебры, использующие эти операции и объекты.

## stringolist
Модуль, который позволяет работать со строко-списками - гибрид строки и списка. Является Python-списком, но имеет в себе методы Python-строки. Таким образом можно искать "подсписок" (подстроко-список) у данного строко-списка. Строко-список можно понимать, как Python-строку, которая вместо символов содержит любые объекты.

### Создание строко-списка
Для создания строко-списка в конструктор в качестве параметра нужно подать список, либо подать сразу несколько объектов:
```
s = stringolist(0, 1.1, 'abc', None)            # stringolist([0, 1.1, 'abc', None])
print(len(s))                                   # 4
helloList = stringolist(list('Hello world!'))   # stringolist(['H', 'e', 'l', 'l', 'o', ' ', 'w', 'o', 'r', 'l', 'd', '!'])
print(len(helloList))                           # 12
helloStr = stringolist('Hello world')           # stringolist(['Hello world'])
print(len(helloStr))                            # 1
```
Количество параметров, поданных в конструктор, приоритетнее значения первого параметра:
```
a = stringolist([1, 2, 3], 'abc')   # stringolist([[1, 2, 3], 'abc'])
print(len(a))                       # 2
b = stringolist([[1, 2, 3]])        # stringolist([[1, 2, 3]])
print(len(b))                       # 1
```

### Операции над строко-списками
Операции сложения и умножения над строко-списками такие же как и над строками или списками в Python.
```
a = stringolist(1, 2, 3)    # stringolist([1, 2, 3])
b = stringolist(4, 5, 6)    # stringolist([4, 5, 6])
print(a + b)                # stringolist([1, 2, 3, 4, 5, 6])
print(a * 3)                # stringolist([1, 2, 3, 1, 2, 3, 1, 2, 3])
print(b * 0)                # stringolist([])
print(b * -1)               # stringolist([])
```

### Получение объекта по ключу или срезу
Получение объекта по ключу или срезу работает как и для строк или списков:
```
L = ['a', 'b', 'c', 'd', 'e', 'f']
S = stringolist(L.copy())           # чтобы случайно не изменить строко-список через переменную L, делаем её копию
print(S[0])                         # a
print(S[3])                         # d
print(S[-1])                        # f
print(S[-4])                        # c
print(S[1:4])                       # stringolist(['b', 'c', 'd'])
print(S[:2])                        # stringolist(['a', 'b'])
print(S[3:])                        # stringolist(['d', 'e', 'f'])
print(S[::2])                       # stringolist(['a', 'c', 'e'])
```

### Перечисление в цикле *for*
Можно в цикле *for* поработать с каждым объектом данного строко-списка:
```
nums = stringolist(list(range(10))) # stringolist([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
sqrs = stringolist()                # stringolist([])
for num in nums:
    sqrs.append(num ** 2)
print(sqrs)                         # stringolist([0, 1, 4, 9, 16, 25, 36, 49, 64, 81])
```

### Проверка принадлежности
Проверка принадлежности работает как для строки:
```
s = stringolist(0, 'f', 23, 4.5, -0.0, None)    # stringolist([0, 'f', 23, 4.5, -0.0, None])
sub = stringolist('f', 23, 4.5)                 # stringolist(['f', 23, 4.5])
print(sub in s)                                 # True
sub = stringolist('f', 4.5)                     # stringolist(['f', 4.5])
print(sub in s)                                 # False
print(23 in s)                                  # TypeError: must be stringolist, not int
```

## exprtree
Модуль, который позволяет создавать свои операции
