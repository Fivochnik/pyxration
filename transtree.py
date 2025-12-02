from exprtree import exprtree
from functree import functree, funcparam

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
    """Сортирует существующий список, используя функцию линейного строгого порядка."""
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
            cmp_s = cmp(v, min_v)
            if cmp_s == -1:
                min_v = v
                min_i = i
                continue
            cmp_e = cmp(v, max_v)
            if cmp_e == 1:
                max_v = v
                max_i = i
        if min_i == last:
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

formula является кортежом из двух экземпляров класса functree с одним и тем же набором параметров, даже если в одном из них какие-то параметры вообще не используются.
"""
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
    from cmpall import cmp
    
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
    p0 = '%x%+0'
    p1 = '%x%*1'
    p = '%x%'
    p0st = stringolist(list(p0))
    p1st = stringolist(list(p1))
    pst = stringolist(list(p))
    p0func = simple.new_func(p0st, [funcparam('x')])
    p1func = simple.new_func(p1st, [funcparam('x')])
    pfunc = simple.new_func(pst, [funcparam('x')])
    Plus0 = p0func, pfunc
    Mult1 = p1func, pfunc
    neutralPlus = expression_replacer(Plus0)
    neutralMult = expression_replacer(Mult1)

    a = '12+(0+1*k)+9*a+1*(a+b*(0+k))+12*b+3'
    b = '12+3+9*a+12*b+(k*1+0)+1*(a+b*(k+0))'
    ast = stringolist(list(a))
    bst = stringolist(list(b))
    aExpr = simple.new_expr(ast)
    bExpr = simple.new_expr(bst)
    simple.order_brackets_del(aExpr)
    simple.order_brackets_del(bExpr)
    print('-' * 50)
    print(f'a = {a} = {simple.to_str(aExpr)}:\n{str_tree(aExpr)}')
    print('-' * 50)
    print(f'b = {b} = {simple.to_str(bExpr)}:\n{str_tree(bExpr)}')
    print('-' * 50)
    aExpr = apply(aExpr, sortPlusMult)
    bExpr = apply(bExpr, sortPlusMult)
    print('\n' * 9)
    print('-' * 50)
    print(f'a = {a} = {simple.to_str(aExpr)}:\n{str_tree(aExpr)}')
    print('-' * 50)
    print(f'b = {b} = {simple.to_str(bExpr)}:\n{str_tree(bExpr)}')
    print('-' * 50)
    aExpr = apply(aExpr, neutralPlus)
    bExpr = apply(bExpr, neutralPlus)
    aExpr = apply(aExpr, neutralMult)
    bExpr = apply(bExpr, neutralMult)
    print('\n' * 9)
    print('-' * 50)
    print(f'a = {a} = {simple.to_str(aExpr)}:\n{str_tree(aExpr)}')
    print('-' * 50)
    print(f'b = {b} = {simple.to_str(bExpr)}:\n{str_tree(bExpr)}')
    print('-' * 50)
