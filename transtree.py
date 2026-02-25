from exprtree import exprtree, operation
from functree import functree, funcparam
from cmpall import cmp

def apply(main: 'exprtree|functree|any', trans: 'func(exprtree|any) -> exprtree|any') -> 'exprtree|functree|any':
    if isinstance(main, functree):
        return apply(main.val, trans)
    elif not isinstance(main, exprtree):
        return trans(main)
    else:
        for i, tree in enumerate(main.trees):
            main.trees[i] = apply(tree, trans)
        return trans(main)
apply.__doc__ = """Применяет преобразование trans к каждому подвыражению выражения main.
Возвращает результат преобразования.

main - дерево-выражение или дерево-функция, которое мы хотим изменить.
Само выражение main может поменяться. Нужно сделать копию дерева, чтобы сохранить выражение.

trans - функция, которая принимает на вход только один аргумент - дерево-выражение или отличный от узла дерева объект и """ + \
"""проводит изменение на данном узле (листе) без рекурсивного хода, если это возможно, и возвращает результат преобразования.
Важно! Даже если выражение не поменялось нужно вернуть его самого, а не None или что-либо ещё."""

def sortList(lst: list, cmp: 'func(any, any) -> int' = None, reverse: bool = False):
    """Сортирует существующий список, используя функцию линейного строгого порядка.
lst - список объектов, который нужно просортировать;
cmp - функция сравнения пары объектов: -1 - первый аргумент меньше второго, 1 - первый аргумент больше второго, 0 - аргументы равны;
reverse - флаг, который определяет порядок сортировки: False - от меньшего к большему, True - от большего к меньшему."""
    if cmp is None:
        cmp = lambda a, b: -1 if a < b else 0 if a == b else 1
    if reverse:
        __cmp__ = cmp
        cmp = lambda a, b: -__cmp__(a, b)
    lst_len = len(lst)
    for start in range(lst_len // 2):
        end = lst_len - start
        last = end - 1
        min_i = max_i = start
        min_v = max_v = lst[start]
        for i in range(start, end):
            v = lst[i]
            if cmp(v, min_v) == -1:
                min_v = v
                min_i = i
            elif cmp(v, max_v) == 1:
                max_v = v
                max_i = i
        if min_i == max_i:
            return
        elif min_i == last:
            if max_i == start:
                lst[start], lst[last] = min_v, max_v
            else:
                lst[start], lst[min_i] = min_v, lst[start]
                if max_i != last:
                    lst[last], lst[max_i] = max_v, lst[last]
        elif max_i == start:
            lst[last], lst[max_i] = max_v, lst[last]
            if min_i != start:
                lst[start], lst[min_i] = min_v, lst[start]
        else:
            if min_i != start:
                lst[start], lst[min_i] = min_v, lst[start]
            if max_i != last:
                lst[last], lst[max_i] = max_v, lst[last]

def operation_sorter(operList: list) -> 'func(exprtree|any) -> exprtree|any':
    """Создаёт функцию, которая сортирует аргументы операций из списка operList.
operList - список уже созданных операций.
Возвращает созданную функцию."""

    def sortedExpr(main: 'exprtree|any') -> 'exprtree|any':
        """Сортирует аргументы некоторых операций.
Возвращает выражение с сортированными аргументами операций или без изменений."""
        if not isinstance(main, exprtree):
            return main
        oper = main.val
        trees = main.trees
        if oper in operList:
            sortList(trees, cmp)
        return main

    return sortedExpr

def expression_replacer(formula: tuple) -> 'func(exprtree|any) -> exprtree|any':
    """Создаёт функцию, которая заменяет выражение, если оно похожа на первую часть формулы, на другое выражение из второй части формулы.
formula - пара функций-деревьев с одинаковым набором параметров.
Возвращает созданную функцию.

formula является кортежом из двух экземпляров класса functree с одним и тем же набором параметров, даже если в одном из них какие-то параметры вообще не используются."""
    if not isinstance(formula, tuple):
        raise TypeError(f'единственный аргумент функции должен быть кортежом, а не объектом типа "{type(formula).__name__}"')
    if len(formula) != 2:
        raise ValueError(f'единственный аргумент функции должен быть кортежом из двух объектов, а не из "{len(formula)}"')
    left, right = formula
    if not (isinstance(left, functree) and isinstance(right, functree)):
        raise TypeError(f'единственный аргумент функции должен быть кортежом из двух экземпляров класса functree, а не из "{type(left).__name__}" и "{type(right).__name__}"')
    if left.params != right.params:
        raise ValueError(f'оба объекта из аргумента должны иметь одинаковый набор параметров')

    def replacedExpr(main: 'exprtree|any') -> 'exprtree|any':
        """Заменяет выражение по заранее заданному шаблону.
Возвращает заменённое или оставленное без изменений выражение."""
        params = {}
        if left.paramvals(main, params):
            res = right.copy().subs(params)
            if isinstance(main, functree):
                main.expr = res.expr
                for p in res.params:
                    if not p in main.params:
                        main.params.append(p)
            else:
                main = res.expr
        return main

    return replacedExpr

def neutrals_deleter(neutrals: dict) -> 'func(exprtree|any) -> exprtree|any':
    """Создаёт функцию, которая удаляет нейтральные элементы операций.
neutrals - словарь, ключами которого являются имена операций, а значениями - списки элементов, которые считаются нейтральными для данной операции.
Возвращает созданную функцию."""
    if not isinstance(neutrals, dict):
        raise TypeError(f'единственный аргумент функции должен быть словарём, а не объектом типа "{type(neutrals).__name__}"')
    for op, ne in neutrals.items():
        if not isinstance(op, str):
            raise TypeError(f'ключи словаря должны быть строками, а не объектом типа "{type(op).__name__}"')
        if not isinstance(ne, list):
            raise TypeError(f'значения словаря должны быть списками, а не объектом типа "{type(ne).__name__}"')

    def withoutNeutrals(main: 'exprtree|any') -> 'exprtree|any':
        """Удаляет заранее заданные нейтральные элементы.
Возвращает изменённое или оставленное без изменений выражение."""
        if not isinstance(main, exprtree):
            return main
        oper_name = main.val.name
        if oper_name in neutrals.keys():
            trees = []
            ns = neutrals[oper_name]
            for tree in main.trees:
                if not tree in ns:
                    trees.append(tree)
            trees_len = len(trees)
            if trees_len == 0:
                return ns[0]
            elif trees_len == 1:
                return trees[0]
            main.trees = trees
        return main

    return withoutNeutrals

def zero_absorber(zeros: dict) -> 'func(exprtree|any) -> exprtree|any':
    """Создаёт функцию, которая "зануляет" операции, содержащие "нуль-элемент".
zeros - словарь, ключами которого являются имена операций, а значениями - списки элементов, которые считаются "нулями" для данной операции.
Возвращает созданную функцию."""
    if not isinstance(zeros, dict):
        raise TypeError(f'единственный аргумент функции должен быть словарём, а не объектом типа "{type(zeros).__name__}"')
    for op, ne in zeros.items():
        if not isinstance(op, str):
            raise TypeError(f'ключи словаря должны быть строками, а не объектом типа "{type(op).__name__}"')
        if not isinstance(ne, list):
            raise TypeError(f'значения словаря должны быть списками, а не объектом типа "{type(ne).__name__}"')

    def absorbed(main: 'exprtree|any') -> 'exprtree|any':
        """Зануляет заранее заданные операции, содержащие "нуль-элементы".
Возвращает изменённое или оставленное без изменений выражение."""
        if not isinstance(main, exprtree):
            return main
        oper_name = main.val.name
        if oper_name in zeros.keys():
            zs = zeros[oper_name]
            for tree in main.trees:
                if tree in zs:
                    return zs[0]
        return main

    return absorbed

def left_associater(operList: list) -> 'func(exprtree|any) -> exprtree|any':
    """Создаёт функцию, которая превращает указанные в списке операции в строго бинарные с выполнением выражения слева-направо.
operList - список операций, которые изначально парсились в строке, как n-арныяе, но нужно перевести в бинарные с учётом левой ассоциативности.
Возвращает созданную функцию."""
    if not isinstance(operList, list):
        raise TypeError(f'единственный аргумент функции должен быть списком, а не объектом типа "{type(operList).__name__}"')
    for op in operList:
        if not isinstance(op, operation):
            raise TypeError(f'элементы списка должны быть объектами типа "operation", а не объектом типа "{type(op).__name__}"')

    def associated(main: 'exprtree|any') -> 'exprtree|any':
        """Превращает заранее заданные операции в строго бинарные с выполнением выражения слева-направо.
Возвращает изменённое или оставленное без изменений выражение."""
        if not isinstance(main, exprtree) or main.trees is None or len(main.trees) < 3:
            return main
        oper = main.val
        trees = main.trees
        res = exprtree(oper, trees[:2])
        for tree in trees[2:]:
            res = exprtree(oper, [res, tree])
        return res

    return associated

def right_associater(operList: list) -> 'func(exprtree|any) -> exprtree|any':
    """Создаёт функцию, которая превращает указанные в списке операции в строго бинарные с выполнением выражения справа-налево.
operList - список операций, которые изначально парсились в строке, как n-арныяе, но нужно перевести в бинарные с учётом правой ассоциативности.
Возвращает созданную функцию."""
    if not isinstance(operList, list):
        raise TypeError(f'единственный аргумент функции должен быть списком, а не объектом типа "{type(operList).__name__}"')
    for op in operList:
        if not isinstance(op, operation):
            raise TypeError(f'элементы списка должны быть объектами типа "operation", а не объектом типа "{type(op).__name__}"')

    def associated(main: 'exprtree|any') -> 'exprtree|any':
        """Превращает заранее заданные операции в строго бинарные с выполнением выражения справа-налево.
Возвращает изменённое или оставленное без изменений выражение."""
        if not isinstance(main, exprtree) or main.trees is None or len(main.trees) < 3:
            return main
        oper = main.val
        trees = main.trees
        res = exprtree(oper, trees[-2:])
        for tree in trees[:-2][::-1]:
            res = exprtree(oper, [tree, res])
        return res

    return associated

if __name__ == '__main__':
    from stringolist import stringolist
    from exprtree import (
        algebra,
        operation,
        operInfix,
        operGrouping,
        operPrefix,
        operObject,
        str_tree
    )
    
    plus = operInfix('plus', '+')
    mult = operInfix('multiply', '*')
    main_group = operGrouping('()', '(', ')')
    intObj = operObject('integer', lambda x: x.is_str() and x.to_str().isdigit(), lambda x: int(x.to_str()), lambda x: stringolist(list(str(x))))
    varObj = operObject('variable', lambda x: x.is_str() and x.to_str().isidentifier(), lambda x: x.to_str(), lambda x: stringolist(list(x)))

    simple = algebra(
        'simple',
        [main_group, plus, mult, intObj, varObj],
        [main_group, intObj, varObj, mult, plus],
        main_group
    )

    sortPlusMult = operation_sorter([plus, mult])
    d0 = '(%b%+%c%)*%a%'
    d1 = '%a%*%b%+%a%*%c%'
    d0st = stringolist(list(d0))
    d1st = stringolist(list(d1))
    d0func = simple.new_func(d0st, [funcparam('a'), funcparam('b'), funcparam('c')])
    d1func = simple.new_func(d1st, [funcparam('a'), funcparam('b'), funcparam('c')])
    simple.order_brackets_del(d0func)
    simple.order_brackets_del(d1func)
    distr = d0func, d1func
    distrToSum = expression_replacer(distr)
    ZERO = exprtree(intObj, [0])
    ONE = exprtree(intObj, [1])
    delNeutrals = neutrals_deleter({'plus': [ZERO], 'multiply': [ONE]})
    absorbed = zero_absorber({'multiply': [ZERO]})

    a = '12+(0+1*k)+9*a+1*0*(a+b*(0+k)*1)+12*b+3+0+a*(b+c)'
    b = '12+1*1*1*0+3+9*a+12*b+(k*1+0)+a*(b+c)+1*(a+b*(k+0))*0'
    ast = stringolist(list(a))
    bst = stringolist(list(b))
    aExpr = simple.new_expr(ast)
    bExpr = simple.new_expr(bst)
    simple.order_brackets_del(aExpr)
    simple.order_brackets_del(bExpr)
    print('-' * 50)
    print(f'A: {a} = {simple.to_str(aExpr)}:\n{str_tree(aExpr, True)}')
    print('-' * 50)
    print(f'B: {b} = {simple.to_str(bExpr)}:\n{str_tree(bExpr, True)}')
    print('-' * 50)
    aExpr = apply(aExpr, sortPlusMult)
    bExpr = apply(bExpr, sortPlusMult)
    print('\n' * 9)
    print('-' * 50)
    print(f'A: {a} = {simple.to_str(aExpr)}:\n{str_tree(aExpr, True)}')
    print('-' * 50)
    print(f'B: {b} = {simple.to_str(bExpr)}:\n{str_tree(bExpr, True)}')
    print('-' * 50)
    aExpr = apply(aExpr, absorbed)
    bExpr = apply(bExpr, absorbed)
    print('\n' * 9)
    print('-' * 50)
    print(f'A: {a} = {simple.to_str(aExpr)}:\n{str_tree(aExpr, True)}')
    print('-' * 50)
    print(f'B: {b} = {simple.to_str(bExpr)}:\n{str_tree(bExpr, True)}')
    print('-' * 50)
    aExpr = apply(aExpr, delNeutrals)
    bExpr = apply(bExpr, delNeutrals)
    print('\n' * 9)
    print('-' * 50)
    print(f'A: {a} = {simple.to_str(aExpr)}:\n{str_tree(aExpr, True)}')
    print('-' * 50)
    print(f'B: {b} = {simple.to_str(bExpr)}:\n{str_tree(bExpr, True)}')
    print('-' * 50)
    aExpr = apply(aExpr, distrToSum)
    bExpr = apply(bExpr, distrToSum)
    print('\n' * 9)
    print('-' * 50)
    print(f'A: {a} = {simple.to_str(aExpr)}:\n{str_tree(aExpr, True)}')
    print('-' * 50)
    print(f'B: {b} = {simple.to_str(bExpr)}:\n{str_tree(bExpr, True)}')
    print('-' * 50)
    simple.order_brackets_del(aExpr)
    simple.order_brackets_del(bExpr)
    print('\n' * 9)
    print('-' * 50)
    print(f'A: {a} = {simple.to_str(aExpr)}:\n{str_tree(aExpr, True)}')
    print('-' * 50)
    print(f'B: {b} = {simple.to_str(bExpr)}:\n{str_tree(bExpr, True)}')
    print('-' * 50)
    
    print(aExpr == bExpr)
