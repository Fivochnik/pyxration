from stringolist import stringolist

def invertOperPreparser(notation: str, invnotation: str, starts: list = None) -> 'stringolist':
    """Создаёт функцию препрарсировки строкового выражения. Созданная функция дописывает обратную инфиксную операцию перед текущей.
notation - обозначение текущей унарной операции, которая может быть представлена как инфиксная;
invnotation - обозначение обратной операции к текущей, которая будет ставиться перед текущей операцией, когда текущая используется как инфиксная;
starts - список обозначений начала подвыражения.

notation и invnotation строко-списоки обозначений обратных друг другу операций, где notation - обозначение операции, которая в операционном дереве будет приниматься как префиксная.

starts - список строко-списков всевозможных начал подвыражений, таких как различные открывающиеся скобки или целые слова."""
    if not isinstance(notation, str):
        raise TypeError(f'первый аргумент функции должен быть объектом класса "str", а не "{type(notation).__name__}"')
    if not isinstance(invnotation, str):
        raise TypeError(f'второй аргумент функции должен быть объектом класса "str", а не "{type(invnotation).__name__}"')
    if starts is None:
        starts = []
    else:
        starts = starts.copy()
    if not isinstance(starts, list):
        raise TypeError(f'аргумент starts должен быть списком, а не объектом класса "{type(starts).__name__}"')
    for n, s in enumerate(starts):
        if not isinstance(s, str):
            raise ValueError(f'элементы списка starts должны быть объектами класса "str", а не "{type(s).__name__}"')
        starts[n] = stringolist(list(s))
    notation = stringolist(list(notation))
    invnotation = stringolist(list(invnotation))

    def invOperPreparse(expr: 'stringolist') -> 'stringolist':
        """Заменяет все инфиксные записи унарной операции обратной операцией с данной операцией после."""
        res = stringolist(expr[0])
        expr_len = len(expr)
        for i in range(1, expr_len):
            if expr.startswith(notation, i):
                if any(expr.endswith(s, 0, i)
                       for s in starts):
                    pass
                else:
                    res += invnotation
            res.append(expr[i])
        return res

    return invOperPreparse

def invertOperPoststringifier(notation: str, invnotation: str) -> 'stringolist':
    """Создаёт функцию обработки строкового выражения перед её возвратом. Созданная функция уберает лишнюю обратную инфиксную операцию перед текущей.
notation - обозначение текущей унарной операции, которая может быть представлена как инфиксная;
invnotation - обозначение обратной операции к текущей, которая будет убираться перед текущей операцией, когда текущая используется как префиксная.

notation и invnotation строко-списоки обозначений обратных друг другу операций, где notation - обозначение операции, которая в операционном дереве будет приниматься как префиксная."""
    if not isinstance(notation, str):
        raise TypeError(f'первый аргумент функции должен быть объектом класса "str", а не "{type(notation).__name__}"')
    if not isinstance(invnotation, str):
        raise TypeError(f'второй аргумент функции должен быть объектом класса "str", а не "{type(invnotation).__name__}"')

    def invOperPoststringify(expr: str) -> str:
        """Заменяет подряд стоящие друг за другом инфиксную обратную и префиксную текущую операции текущей."""
        res = expr.replace(invnotation + notation, notation)
        return res

    return invOperPoststringify

if __name__ == '__main__':
    from exprtree import algebra, exprtree, operation, \
         str_tree, operInfix, operGrouping, operPrefix, operObject

    left = ['(', '[', '{']
    treeer = invertOperPreparser('-', '+', left)
    stringer = invertOperPoststringifier('-', '+')

    plus = operInfix('addition', '+')
    minus = operPrefix('negative', '-')
    group = {
        x: operGrouping(x, *x)
        for x in ['()', '[]', '{}']
    }
    var = operObject('variable', lambda x: x.is_str() and x.to_str().isidentifier(), lambda x: x.to_str(), lambda x: stringolist(list(x)))
    simple = algebra(
        'simple',
        list(group.values()) + [plus, minus, var],
        list(group.values()) + [var, minus, plus],
        group['()'],
        [treeer],
        [stringer]
    )
    
    expr = '-a-b+c-[-a-b]-c'
    exprt = simple.new_expr(expr)
    print(f'{expr}: {simple.to_str(exprt)}\n{str_tree(exprt)}')
