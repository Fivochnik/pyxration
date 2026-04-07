from stringolist import stringolist
import exprtree
import functree
import transtree

#Введение констант:
stringolist_true = stringolist('1')
stringolist_false = stringolist('0')

#Создание операций и объектов:
OpNot = exprtree.operPrefix('not', '~')
OpAnd = exprtree.operInfix('and', '&')
OpOr = exprtree.operInfix('or', '|')
OpXor = exprtree.operInfix('xor', '^')
OpImp = exprtree.operInfix('implication', '->')

def is_bool(x: stringolist):
    """Определяет, может ли строко-список быть логическим значением"""
    return x in [stringolist_true, stringolist_false]

def to_bool(x: stringolist):
    """Переводит строко-список в логическое значение и возвращает его."""
    return x == stringolist_true

def bool_to_stringolist(x: bool):
    """Переводит логическое значение в строко-список и возвращает его."""
    return stringolist_true if x else stringolist_false

def is_variable(x: stringolist):
    """Опеределяет, может ли строко-список быть именем переменной.
Возвращает True, если строко-список может быть именем переменной, иначе - False."""
    return x.is_str() and x.to_str().isidentifier()

def to_variable(x: stringolist):
    """Переводит строко-список в переменную и возвращает её."""
    return x.to_str()

def variable_to_stringolist(x: str):
    """Переводит переменную в строко-список и возвращает его."""
    return stringolist(list(x))

ObjBool = exprtree.operObject('boolean',
                              is_bool,
                              to_bool,
                              bool_to_stringolist)
ObjVar = exprtree.operObject('variable',
                             is_variable,
                             to_variable,
                             variable_to_stringolist)
                             
Group = exprtree.operGrouping('()', '(', ')')

#Создание алгебры:
Classic = exprtree.algebra('classic logic',
                           [Group, OpImp, OpOr, OpXor, OpAnd, OpNot, ObjBool, ObjVar],
                           [Group, ObjBool, ObjVar, OpNot, OpAnd, OpXor, OpOr, OpImp],
                           Group)

#Создание преобразований выражений:
ObjFalse = Classic.new_expr('0')
ObjTrue = Classic.new_expr('1')
del_neutrals = transtree.neutrals_deleter(
    {'and': [ObjTrue],
     'or': [ObjFalse],
     'xor': [ObjFalse]}
    )
absorb = transtree.zero_absorber(
    {'and': [ObjFalse],
     'or': [ObjTrue]}
    )
sort = transtree.operation_sorter(
    [OpAnd, OpOr, OpXor]
    )

#Создание выражений:
A_str = 'A^(A&B->D|C)^0^1^Z'
A = Classic.new_expr(A_str)

B_str = '(A|0|B)&(A|1|C)->A&B&1|A&0&C'
B = Classic.new_expr(B_str)

#Вывод выражений:
print(f'A = {Classic.to_str(A)}:\n{exprtree.str_tree(A, True)}')
print(f'B = {Classic.to_str(B)}:\n{exprtree.str_tree(B, True)}')

#Выполнение поглащения:
A = transtree.apply(A, absorb)
B = transtree.apply(B, absorb)

#Вывод выражений:
print(f'A = {Classic.to_str(A)}:\n{exprtree.str_tree(A, True)}')
print(f'B = {Classic.to_str(B)}:\n{exprtree.str_tree(B, True)}')

#Выполнение удаления нейтральных элементов:
A = transtree.apply(A, del_neutrals)
B = transtree.apply(B, del_neutrals)

#Вывод выражений:
print(f'A = {Classic.to_str(A)}:\n{exprtree.str_tree(A, True)}')
print(f'B = {Classic.to_str(B)}:\n{exprtree.str_tree(B, True)}')

#Выполнение сортировки:
A = transtree.apply(A, sort)
B = transtree.apply(B, sort)

#Вывод выражений:
print(f'A = {Classic.to_str(A)}:\n{exprtree.str_tree(A, True)}')
print(f'B = {Classic.to_str(B)}:\n{exprtree.str_tree(B, True)}')
