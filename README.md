# pyxration
Символьная алгебраическая библиотека для создания и описания своих алгебраических систем.

Позволяет создавать свои операции, объекты и алгебры, использующие эти операции и объекты.

## stringolist и его основные методы
Модуль, который позволяет работать со строко-списками - гибрид строки и списка. Является Python-списком, но имеет в себе методы Python-строки. Таким образом можно искать "подсписок" (подстроко-список) у данного строко-списка. Строко-список можно понимать, как Python-строку, которая вместо символов содержит любые объекты.

### Создание строко-списка
Для создания строко-списка в конструктор в качестве параметра нужно подать список, либо подать сразу несколько объектов:
```python
s = stringolist(0, 1.1, 'abc', None)            # stringolist([0, 1.1, 'abc', None])
len(s)                                          # 4
helloList = stringolist(list('Hello world!'))   # stringolist(['H', 'e', 'l', 'l', 'o', ' ', 'w', 'o', 'r', 'l', 'd', '!'])
len(helloList)                                  # 12
helloStr = stringolist('Hello world')           # stringolist(['Hello world'])
len(helloStr)                                   # 1
```
Количество параметров, поданных в конструктор, приоритетнее значения первого параметра:
```python
a = stringolist([1, 2, 3], 'abc')   # stringolist([[1, 2, 3], 'abc'])
len(a)                              # 2
b = stringolist([[1, 2, 3]])        # stringolist([[1, 2, 3]])
len(b)                              # 1
```

### Добавление новых объектов в строко-список
Добавление новых элементов производится так же как и в список:
```python
a = stringolist(list('Hell'))   # stringolist(['H', 'e', 'l', 'l'])
a.append('o')
a                               # stringolist(['H', 'e', 'l', 'l', 'o'])
```

### Операции над строко-списками
Операции сложения и умножения над строко-списками такие же как и над строками или списками в Python.
```python
a = stringolist(1, 2, 3)    # stringolist([1, 2, 3])
b = stringolist(4, 5, 6)    # stringolist([4, 5, 6])
a + b                       # stringolist([1, 2, 3, 4, 5, 6])
a * 3                       # stringolist([1, 2, 3, 1, 2, 3, 1, 2, 3])
b * 0                       # stringolist([])
b * -1                      # stringolist([])
```

### Получение объекта по ключу или срезу
Получение объекта по ключу или срезу работает как и для строк или списков:
```python
L = ['a', 'b', 'c', 'd', 'e', 'f']
S = stringolist(L.copy())           # чтобы случайно не изменить строко-список через переменную L, делаем её копию
S[0]                                # 'a'
S[3]                                # 'd'
S[-1]                               # 'f'
S[-4]                               # 'c'
S[1:4]                              # stringolist(['b', 'c', 'd'])
S[:2]                               # stringolist(['a', 'b'])
S[3:]                               # stringolist(['d', 'e', 'f'])
S[::2]                              # stringolist(['a', 'c', 'e'])
```

### Перечисление в цикле *for*
Можно в цикле *for* поработать с каждым объектом данного строко-списка:
```python
nums = stringolist(list(range(10))) # stringolist([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
sqrs = stringolist()                # stringolist([])
for num in nums:
    sqrs.append(num ** 2)
sqrs                                # stringolist([0, 1, 4, 9, 16, 25, 36, 49, 64, 81])
```

### Проверка принадлежности
Проверка принадлежности работает как для строки:
```python
s = stringolist(0, 'f', 23, 4.5, 'abc', None)   # stringolist([0, 'f', 23, 4.5, 'abc', None])
sub = stringolist('f', 23, 4.5)                 # stringolist(['f', 23, 4.5])
sub in s                                        # True
sub = stringolist('f', 4.5)                     # stringolist(['f', 4.5])
sub in s                                        # False
23 in s                                         # TypeError: must be stringolist, not int
```

### Поиск объектов и подстроко-списков
Для поиска объектов в строко-списке как в списке используется метод *index*, а для поиска подстроко-списка используются *find* и *rfind*:
```python
s = stringolist(0, 1, 2, 0, 1, 2, 0, 1, 2)      # stringolist([0, 1, 2, 0, 1, 2, 0, 1, 2])
s.index(2)                                      # 2
sub = stringolist(2, 0, 1)                      # stringolist([2, 0, 1])
s.find(sub)                                     # 2
s.rfind(sub)                                    # 5
```

### Замена подстроко-списка другим
Замена подстрокосписка другим производится методом *replace*. Сам строко-список не изменится. Этот метод работает подобно методу для строки:
```python
s = stringolist(list('apple  orange  watermelon'))  # stringolist(['a', 'p', 'p', 'l', 'e', ' ', ' ', 'o', 'r', 'a', 'n', 'g', 'e', ' ', ' ', 'w', 'a', 't', 'e', 'r', 'm', 'e', 'l', 'o', 'n'])
old = stringolist(list('  '))                       # stringolist([' ', ' '])
new = stringolist(list(', '))                       # stringolist([',', ' '])
s.replace(old, new)                                 # stringolist(['a', 'p', 'p', 'l', 'e', ',', ' ', 'o', 'r', 'a', 'n', 'g', 'e', ',', ' ', 'w', 'a', 't', 'e', 'r', 'm', 'e', 'l', 'o', 'n'])
new = stringolist(list(' '))                        # stringolist([' '])
s.replace(old, new)                                 # stringolist(['a', 'p', 'p', 'l', 'e', ' ', 'o', 'r', 'a', 'n', 'g', 'e', ' ', 'w', 'a', 't', 'e', 'r', 'm', 'e', 'l', 'o', 'n'])
```

### Разбитие строко-списка на строко-списки
Разбитие строко-списка на строко-списки производится методом *split*, как это делается и для строк:
```python
s = stringolist(list('apple  orange  watermelon'))  # stringolist(['a', 'p', 'p', 'l', 'e', ' ', ' ', 'o', 'r', 'a', 'n', 'g', 'e', ' ', ' ', 'w', 'a', 't', 'e', 'r', 'm', 'e', 'l', 'o', 'n'])
sep = stringolist(list('  '))                       # stringolist([' ', ' '])
s.split(sep)                                        # [stringolist(['a', 'p', 'p', 'l', 'e']), stringolist(['o', 'r', 'a', 'n', 'g', 'e']), stringolist(['w', 'a', 't', 'e', 'r', 'm', 'e', 'l', 'o', 'n'])]
```

## exprtree и его основные методы
Модуль, который позволяет создавать свои операции, строить с помощью них алгебру и задавать выражения с помощью уже алгебры.

### Класс *operation*
Экземпляры класса *operation* - операции. Их можно создать, если подать в конструктор имя операции (и функции парсировки и представления операции в строковом выражении, если они имеются):
```python
addition = operation('addition')
multiplication = operation('multiplication')
```

Для добавления функции парсировки и представления операции достаточно подать эти функции в метод "funcs_update" по одному или в кортеже. Есть готовые шаблоны этих функций, можно воспользоваться ими:
```python
addition.funcs_update(infix_parser_and_repres('+', addition))
multiplication.funcs_update(infix_parser_and_repres('*', multiplication))
```

Сама по себе операция больше ничего не представляет.

### Класс *algebra*
Экземпляры класса *algebra* - алгебры со своими операциями и правилами. Их можно создать, если подать в конструктор имя алгебры и список операций, который задаёт порядок парсировки этих операций в строковом выражении. Также можно подать список операций, который задаёт порядок выполнения выражения, и группирующую операцию, чтобы сгруппировать подвыражения, тем самым задав порядок выполнения выражения.
```python
simple_algebra = algebra('simple', [addition, multiplication])
```

### Класс *exprtree*
Экземпляры класса *exprtree* - операционные деревья выражений. Их можно создать, используя готовую алгебру, вызвав метод *new_expr* со строко-списком в качестве параметра:
```python
expr_str = 'x+y*z'
expr_SL = stringolist(list(expr_str))
expr = simple_algebra.new_expr(expr_SL)
```

Функция *str_tree* вернёт строковое представления операционного дерева выражения на боку:
```python
print(str_tree(expr))
```
```
[addition]
├x
└[multiplication]
 ├y
 └z
```
