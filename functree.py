from stringolist import stringolist
from exprtree import operation, algebra, exprtree, str_tree
from exprtree import infix_parser_and_repres, grouping_parser_and_repres, prefix_parser_and_repres, object_parser_and_repres

class funcparam:
    """Класс параметра функции.
name - уникальное имя параметра.

Имя параметра должно быть уникальным в рамках самой функции."""

    __slots__ = ['name']

    def __init__(self, name: str):
        if not isinstance(name, str):
            raise TypeError(f'имя параметра должно быть строкой, а не "{type(name).__name__}"')
        self.name = name

    def __eq__(self, other):
        return isinstance(other, funcparam) and self.name == other.name

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'funcparam({self.name})'

    def __reduce__(self):
        return self.__class__, (self.name,)

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
                fp = funcparam(expr[opened + 1:i].to_str())
                if not fp in params:
                    params.append(fp)
                new_expr.append(fp)
                opened = None
        elif opened is None:
            new_expr.append(obj)
    if not opened is None:
        raise SyntaxError('ожидался закрывающий "%", но его не было встречено')
    r11 = stringolist('\\\\'), stringolist('\\')
    r1p = stringolist('\\%'), stringolist('%')
    new_expr = new_expr.replace(*r1p).replace(*r11)
    res = functree(self.new_expr(new_expr), params)
    res = _normalizefunc(res)
    return res

def _normalizefunc(func: 'functree|exprtree') -> 'functree|exprtree':
    """Приводит параметры функции к нормальному виду.
В конце работы функции "new_func" функция-дерево содержит свои параметры в виде одноэлементного строко-списка с этим самым параметром.
Данная функция исправляет это недоразумение, вытаскивая параметр из строко-списка."""
    if isinstance(func, functree):
        func.expr = _normalizefunc(func.expr)
    elif isinstance(func, exprtree):
        func_len = len(func.trees)
        for i in range(func_len):
            cur = func.trees[i]
            if isinstance(cur, stringolist):
                if len(cur) == 1 and isinstance(cur[0], funcparam):
                    func.trees[i] = cur[0]
            else:
                func.trees[i] = _normalizefunc(cur)
    elif isinstance(func, stringolist):
        if len(func) == 1 and isinstance(func[0], funcparam):
            return func[0]
    return func

algebra.new_func = new_func
del new_func

class functree:

    __slots__ = ['expr', 'params']

    def __init__(self, val: 'exprtree', params: list):
        self.expr = val
        self.params = params

    def __reduce__(self):
        return self.__class__, (self.expr, []), None, iter(self.params)

    def copy(self):
        """Возвращает копию функции-дерева."""
        return functree(self.expr.copy() if hasattr(self.expr, 'copy') else self.expr, self.params.copy())

    def paramvals(self, expr: 'exprtree|functree', params: dict = None) -> bool:
        """Определяет значения параметров, при которых функция будет эквивалентна выражению.
Возвращает True, если такие значения можно подобрать, иначе - False.
expr - операционное дерево или дерево-функция, с которым сравнивается функция-дерево;
params - словарь определённых значений параметров.

expr - операционное дерево или дерево-функция - должно полностью совпадать с текущей функцией, кроме, быть может узлов, где у функции стоят параметры,
чтобы функция подобрала значения для параметров.

params - словарь вида {str: exprtree}, где ключами являются имена параметров функции, а значениями - операционные деревья - значения параметров.
"""
        if isinstance(self, functree):
            if params is None:
                params = {}
            res = functree.paramvals(self.expr, expr, params)
            if res:
                for p in params.keys():
                    param = params[p]
                    if hasattr(param, 'copy'):
                        params[p] = param.copy()
            return res
        elif isinstance(self, funcparam):
            if self.name in params.keys():
                if params[self.name] != expr:
                    return False
            else:
                params[self.name] = expr
            return True
        elif isinstance(self, exprtree):
            self_len = len(self.trees)
            if not isinstance(expr, exprtree):
                return False
            expr_len = len(expr.trees)
            if self.val == expr.val and self_len == expr_len:
                return all(functree.paramvals(self.trees[i], expr.trees[i], params)
                           for i in range(self_len))
            else:
                return False
        else:
            return self == expr

    def subs(self, params: dict) -> 'exprtree|functree|any':
        """Подставляет значения параметров в функцию-дерево.
params - словарь, где ключи являются именами параметров, а значения - деревья операций.

Само дерево-функция меняется: если нужно сохранить текущее дерево-функцию, сделайте копию перед применением метода."""
        if isinstance(self, functree):
            self.expr = functree.subs(self.expr, params)
            for tree in params.values():
                if isinstance(tree, functree):
                    for p in tree.params:
                        if not p in self.params:
                            self.params.append(p)
        elif isinstance(self, funcparam):
            res = params.get(self.name, None)
            if not res is None:
                if isinstance(res, functree):
                    res = res.expr
                self = res
                if hasattr(res, 'copy'):
                    self = res.copy()
        elif isinstance(self, exprtree):
            for n, tree in enumerate(self.trees):
                self.trees[n] = functree.subs(tree, params)
        return self

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
        expf = simple.new_func(exps)
        print(expr, str_tree(expf, True), sep = ':\n')
        expt = simple.new_expr(exps.replace(stringolist('%'), stringolist()))
        print('\n' + expr.replace('%', ''), str_tree(expt, True), sep = ':\n')
        prms = {}
        print(f'{expf.paramvals(expt, prms) = }')
        for p in prms:
            print(f'{p} = {simple.to_str(prms[p])}\n{str_tree(prms[p])}')
