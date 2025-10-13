from stringolist import stringolist
from exprtree import operation, algebra, exprtree, str_tree
from exprtree import infix_parser_and_repres, grouping_parser_and_repres, prefix_parser_and_repres, object_parser_and_repres

class funcparam:
    """Класс параметра функции.
name - уникальное имя параметра.

Имя параметра должно быть уникальным в рамках самой функции."""

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'funcparam({self.name})'

def new_func(self, expr: 'stringolist', params: list = None) -> 'functree':
    if params is None:
        params = []
    r11 = stringolist('\\', '\\'), stringolist('\\\\')
    r1p = stringolist('\\', '%'), stringolist('\\%')
    new_expr = stringolist()
    opened = None
    for i, obj in enumerate(expr.replace(*r11).replace(*r1p)):
        if obj == '%':
            if opened is None:
                opened = i
            else:
                fp = funcparam(expr[opened + 1:i])
                if not fp in params:
                    params.append(fp)
                new_expr.append(fp)
                opened = None
        elif opened is None:
            new_expr.append(obj)
    if not opened is None:
        raise SyntaxError('ожидался закрывающий "%", но его не было встречено')
    new_expr = new_expr.replace(r1p[1], r1p[0]).replace(r11[1], r11[0])
    return functree(self.new_expr(new_expr), params)

algebra.new_func = new_func
del new_func

class functree:

    def __init__(self, val: 'exprtree', params: list):
        self.expr = val
        self.params = params

if __name__ == '__main__':
    if True:
        group = {x: operation(x) for x in ['()', '[]', '{}']}
        for x in group.keys():
            group[x].funcs_update(grouping_parser_and_repres(x[0], x[1], group[x]))
        split = operation('split')
        split.funcs_update(infix_parser_and_repres(',', split))
        plus = operation('plus')
        plus.funcs_update(infix_parser_and_repres('+', plus))
        minus = operation('minus')
        minus.funcs_update(infix_parser_and_repres('-', minus))
        power = operation('power')
        power.funcs_update(infix_parser_and_repres('^', power))
        sin = operation('sin')
        cos = operation('cos')
        [ x.funcs_update(prefix_parser_and_repres( name,
                                                   x,
                                                   [(group['()'], None)] ))
          for x, name in [(sin, 'sin'), (cos, 'cos')] ]
        root = operation('root')
        root.funcs_update(prefix_parser_and_repres( 'root',
                                                    root,
                                                    [(group['[]'], None), (group['()'], None)] ))
        def is_int_num(s: stringolist) -> bool:
            return s.is_str() and s.to_str().isdigit()
        def to_int_num(s: stringolist) -> int:
            return int(s.to_str())
        def int_num_to_strlst(n: int) -> stringolist:
            return stringolist(list(str(n)))
        int_num = operation('integer')
        int_num.funcs_update(object_parser_and_repres(is_int_num, int_num, to_int_num, int_num_to_strlst))
        def is_var(s: stringolist) -> bool:
            if s.is_str():
                res = s.to_str()
                return res.isidentifier() and not res[0].isdigit()
            return False
        def to_var(s: stringolist) -> str:
            return s.to_str()
        def var_to_strlst(v: str) -> stringolist:
            return stringolist(list(v))
        variable = operation('variable')
        variable.funcs_update(object_parser_and_repres(is_var, variable, to_var, var_to_strlst))
        simple = algebra('simple', [x for x in group.values()] + [split, plus, minus, power, sin, cos, root, int_num, variable])
        expr = 'sin(root[2](%x%))^2+cos(root[2](%x%))^2+[({r,q},e)-root[%n%](78)]'
        exps = stringolist(list(expr))
        expt = simple.new_func(exps)
        print(expr, str_tree(expt), sep = ':\n')
        #print('expr =', simple.to_str(expr))
