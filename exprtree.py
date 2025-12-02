from stringolist import stringolist
from cmpall import cmp, _dumps, _cmp_first_call, _cmp_with_pickle, _cmp_with_dill
from importlib.util import find_spec

class algebra:
    """Класс алгебры математических выражений.
name - уникальное имя алгебры;
operation_parsing_order - порядок обработки строкового выражения парсерами операций;
operation_execution_order - порядок выполнения операций в выражении этой алгебры;
order_brackets - группирующая операция, показывающая порядок выполнения операций.

Имя алгебры должно быть уникальным, если вы хотите хранить ваши алгебры в словарях и избегать их перезаписывания.

Аргумент operation_parsing_order должен быть списком операций.
Положение операций в этом списке показывает порядок, в котором будут выполняться методы парсировки от каждой операции.

Аргумент operation_execution_order должен быть списком операций.
Положение операций в этом списке показывает порядок, в котором будут выполняться операции."""

    __slots__ = ['name', 'oper_pars_ord', 'oper_exec_ord', 'ord_brac']

    def __init__(self,
                 name: str,
                 operation_parsing_order: list,
                 operation_execution_order: list = None,
                 order_brackets: 'oper' = None):
        self.name = name
        self.oper_pars_ord = operation_parsing_order
        self.oper_exec_ord = operation_execution_order
        self.ord_brac = order_brackets

    def __reduce__(self):
        return self.__class__, (self.name, [], self.oper_exec_ord, self.ord_brac), None, iter(self.oper_pars_ord)

    def new_expr(self, expr: 'stringolist|exprtree', computed: list = None) -> 'stringolist|exprtree':
        """Создаёт деревья выражений из строкового выражения."""
        if computed is None:
            computed = []
        if isinstance(expr, exprtree):
            res = expr.copy()
            for n, x in enumerate(res.trees):
                if any(x is y for y in computed):
                    continue
                res.trees[n] = self.new_expr(x)
                computed.append(res.trees[n])
            computed.append(res)
            return res
        #elif isinstance(expr, str):
        #    res = stringolist(list(expr))
        elif not isinstance(expr, stringolist):
            return expr
            #raise TypeError(f'аргумент expr должен быть str, stringolist или exprtree, а не {expr.__class__.__name__}')
        res = expr.copy()
        for oper in self.oper_pars_ord:
            if isinstance(res, exprtree):
                break
            temp_res = oper.parser(res)
            if temp_res is None:
                continue
            res = temp_res
            if isinstance(res, stringolist):
                for n, x in enumerate(res.val):
                    if any(x is y for y in computed):
                        continue
                    res.val[n] = self.new_expr(x)
                    computed.append(res.val[n])
            elif isinstance(res, exprtree):
                for n, x in enumerate(res.trees):
                    if any(x is y for y in computed):
                        continue
                    res.trees[n] = self.new_expr(x)
                    computed.append(res.trees[n])
            computed.append(res)
        return res

    def to_str(self, expr: 'exprtree'):
        """Возвращает математическое выражение в виде строки."""
        if expr is None:
            return ''
        if not isinstance(expr, exprtree):
            return str(expr)
        if self.oper_exec_ord is None:
            def orderOf(oper: 'operation') -> int:
                return -1
        else:
            def orderOf(oper: 'operation') -> int:
                return self.oper_exec_ord.index(oper)# if oper in self.oper_exec_ord else -1
        expr_order = orderOf(expr.val)
        cur_expr_str = exprtree(expr.val, [])
        for i in range(0
                       if expr.trees is None else
                       len(expr.trees)):
            obj_str = self.to_str(expr.trees[i])
            i_order = orderOf(expr.trees[i].val) if isinstance(expr.trees[i], exprtree) else -1
            if i_order != -1 and i_order >= expr_order:
                obj_str = self.ord_brac.repres([obj_str])
            cur_expr_str.trees.append(obj_str)
        return cur_expr_str.val.repres(cur_expr_str.trees)

    def order_brackets_del(self, expr: 'exprtree'):
        """Удаляет все группирующие операции, показывающие порядок выполнения операций.
Должна быть указана операция в атрибуте "ord_brac" для выполнения этого действия.
Если атрибут имеет значение "None", то вернёт "False" и не сделает ничего, иначе - вернёт "True", если хоть одна из группирующий операций была удалена."""
        if self.ord_brac is None or not isinstance(expr, exprtree):
            return False
        deleted = False
        for tree in expr.trees:
            deleted = self.order_brackets_del(tree) or deleted
        if expr.val == self.ord_brac:
            new_expr = expr.trees[0]
            expr.val = new_expr.val
            expr.trees = new_expr.trees
            deleted = True
        return deleted

class exprtree:
    """Класс дерева математического выражения.
val - тип операции или другой объект;
trees - список поддеревьев."""

    __slots__ = ['val', 'trees']

    def __init__(self, val: 'operation', trees: list = None):
        self.val = val
        self.trees = trees

    def __eq__(self, other):
        return isinstance(other, exprtree) and self.val == other.val and self.trees == other.trees

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return self.val.repres(self.trees)

    def __repr__(self):
        return f'exprtree({self.val.name!r}, {self.trees!r})'

    def __reduce__(self):
        if self.trees is None:
            return self.__class__, (self.val,)
        else:
            return self.__class__, (self.val, []), None, iter(self.trees)

    def copy(self):
        """Возвращает копию дерева."""
        return exprtree(self.val, [x.copy() if isinstance(x, exprtree) else x
                                   for x in self.trees])

def str_tree(self: 'functree|exprtree|any', showtypes: bool = False, lasts: list = None, last: bool = False):
    """Возвращает дерево на боку в виде текста."""
    if (self.__class__.__name__ == 'functree' and
        hasattr(self, 'params') and
        hasattr(self, 'expr')):
        return f'{self.params}\n{str_tree(self.expr, showtypes)}'
    if lasts is None:
        lasts = []
    res = ''
    if len(lasts) != 0:
        for l in lasts[:-1]:
            if l:
                res += '│'
            else:
                res += ' '
        res += '└' if last else '├'
    res += f'[{self.val.name}]' if isinstance(self, exprtree) else str(self)
    if showtypes:
        res += f' is {type(self).__name__}'
    res += '\n'
    if isinstance(self, exprtree) and len(self.trees) != 0:
        lasts.append(True)
        for tree in self.trees[:-1]:
            res += str_tree(tree, showtypes, lasts)
        lasts[-1] = False
        res += str_tree(self.trees[-1], showtypes, lasts, True)
        del lasts[-1]
    return res

class operation:

    __slots__ = ['name', 'parser', 'repres']

    def __init__(self,
                 name: str,
                 parser: 'func(str|stringolist) -> exprtree|stringolist|None' = None,
                 repres: 'func(list) -> str' = None,
                 oper_dict: dict = None):
        self.name = name
        self.parser = parser
        self.repres = repres
        if not oper_dict is None:
            oper_dict[self.name] = self

    def __eq__(self, other):
        return self is other

    def __ne__(self, other):
        not self == other

    def __reduce__(self):
        return self.__class__, (self.name,)

    def funcs_update(self,
                     parser: '(func(str|stringolist) -> exprtree|None)|tuple|None' = None,
                     repres: '(func(list) -> str)|None' = None):
        if isinstance(parser, tuple):
            self.parser, self.repres = parser
        else:
            if not parser is None:
                self.parser = parser
            if not repres is None:
                self.repres = repres
operation.__doc__ = (
"""Класс операции.
name - уникальное имя операции;
parser - функция, которая находит текущую операцию и разбивает строку на параметры операции и саму операцию;
repres - функция, которая представляет текущую операцию в виде строки с аргументами этой операции из списка;
oper_dict - словарь операций, в который вы хотите добавить текущую операцию.

Имя операции должно быть уникальным, если вы хотите хранить ваши операции в словарях и избегать их перезаписывания.

Функция "parser" принимает на вход строку или строко-список (stringolist) и возвращает либо exprtree, если ваша """ +
"""операция самая внешняя в строковом выражении, либо stringolist, если обрабатываются внутренние операции, либо """ +
"""None, если вашей операции там нет. Значение None позволяет понять, что строковое выражение не обрабатывалось.
Пример:
def plus_parser(exp: 'str|stringolist') -> 'exprtree|None':
    \"\"\"Обрабатывает строку. Сначала нужно обработать строку на обособляемые операции.\"\"\"
    if isinstance(exp, str):
        exp = stringolist(list(exp))
    elif not isinstance(exp, stringolist):
        raise TypeError(f'Ожидался str или stringolist, а встреченно {exp.__class__.__name__}')
    args = exp.split(stringolist(['+']))
    return exprtree(plus_operation, args) if len(args) > 1 else None
Это позволяет избегать бесконечной рекурсии: если ваша операция не находится в строковом выражении, то функция """ +
"""не должна создавать дерево выражения с единственным параметром необработанного строкового выражения, а вернуть """ +
"""None. Тогда главный парсер пропустит данную операцию и приступит к обработке строкового выражения другой """ +
"""операцией.

Функция "repres" принимает на вход список аргументов этой операции и должна вернуть первоначальное """ +
"""представление данной операции в строковом выражении.
Пример:
def plus_repres(args: list) -> str:
    \"\"\"Создаёт строку математического выражения из списка аргументов операции "+".\"\"\"
    return '+'.join(str(x) for x in args)
В результате должно получиться то же строковое выражение, которое было обработанно функцией "parser".

Можно подать словарь "oper_dict", чтобы записать созданную операцию сразу в словарь. Это может быть полезно, """ +
"""если при написании функции "parser" нужно воспользоваться ещё не созданной операцией. Просто обращаешься по """ +
"""словарю в качестве заглушки, а операция при создании перезапишет себя в словарь.""")

def pair_of(main: stringolist, open_part: stringolist = None, close_part: stringolist = None, pos: int = None):
    """Находит парную часть, соответствующую указанной.
main - главное выражение в виде строко-списка, в котором находится парная часть;
open_part - открывающая часть в виде строко-списка (по-умолчанию: stringolist('('));
close_part - открывающая часть в виде строко-списка (по-умолчанию: stringolist(')'));
pos - положение открывающей или закрывающей части, для которой нужно найти пару (по-умолчанию соответствуюет положению первой встреченной открывающей части).
Возвращает положение парной части в main, или None, если таковая отсутствует.

Пример использования:
expr = 'x+(y*z+(w-x*y)/z)*w'
expr_sl = stringolist(list(expr))
o_p = stringolist('(')
c_p = stringolist(')')
o_p_pos = expr_sl.find(o_p)
fake_c_p_pos = expr_sl.find(c_p) #Найдёт первую попавшуюся ")".
c_p_pos = pair_of(expr_sl, o_p, c_p, o_p_pos) #Найдёт парную закрывающую часть ")"."""
    if not isinstance(main, stringolist):
        raise TypeError(f'первый аргумент функции pair_of должен быть stringolist, а не {main.__class__.__name__}')
    if open_part is None:
        open_part = stringolist('(')
    elif not isinstance(open_part, stringolist):
        raise TypeError(f'аргумент open_part функции pair_of должен быть stringolist, а не {open_part.__class__.__name__}')
    if close_part is None:
        close_part = stringolist(')')
    elif not isinstance(close_part, stringolist):
        raise TypeError(f'аргумент close_part функции pair_of должен быть stringolist, а не {close_part.__class__.__name__}')
    if pos is None:
        pos = main.find(open_part)
    elif not isinstance(pos, int):
        raise TypeError(f'аргумент pos функции pair_of должен быть int, а не {pos.__class__.__name__}')
    counter = None
    if main.startswith(open_part, pos):
        counter = 1
    elif main.startswith(close_part, pos):
        counter = -1
    if counter is None:
        raise ValueError(f'в позиции {pos} не начинается ни окрывающая часть ни закрывающая часть')
    open_part_len = len(open_part)
    close_part_len = len(close_part)
    expr_len = len(main)
    if pos < 0:
        pos += expr_len
    if counter == 1:
        last_index = expr_len - min(open_part_len, close_part_len)
        res = pos + open_part_len
        while counter and res <= last_index:
            if main.startswith(open_part, res):
                counter += 1
                res += open_part_len
            elif main.startswith(close_part, res):
                counter -= 1
                res += close_part_len
            else:
                res += 1
        res -= close_part_len
        return None if counter else res
    else:
        res = pos - close_part_len
        while counter and res >= 0:
            if main.startswith(open_part, res):
                counter += 1
                res -= open_part_len
            elif main.startswith(close_part, res):
                counter -= 1
                res -= close_part_len
            else:
                res -= 1
        res += open_part_len
        return None if counter else res

def infix_parser_and_repres(oper_notation: str, oper: operation) -> ('func(str|stringolist) -> exprtree|None', 'func(list) -> str'):
    """Возвращает функцию-парсер и функцию представления твоей операции.
oper_notation - обозначение инфиксной операции в строковом выражении;
oper - сама операция, у которой ещё нет функций парсеровки и представления.

Для создания своей инфиксной операции нужно:
1. Создать экземпляр операции;
2. Обновить его функции парсировки и представления с помощью этой функции.
Вот, как это выглядит в коде:
addition = operation('addition')
addition.funcs_update(infix_parser_and_repres('+', addition))"""
    def infix_parser(exp: 'str|stringolist') -> 'exprtree|None':
        """Обрабатывает строку."""
        if isinstance(exp, str):
            exp = stringolist(list(exp))
        elif not isinstance(exp, stringolist):
            raise TypeError(f'ожидался str или stringolist, а встреченно {exp.__class__.__name__}')
        args = exp.split(stringolist(list(oper_notation)))
        comp_args = [x[0]
                     if isinstance(x, stringolist) and len(x) == 1 and isinstance(x[0], exprtree) else
                     x
                     for x in args]
        return exprtree(oper, comp_args) if len(comp_args) > 1 else None

    def infix_repres(args: list) -> str:
        """Создаёт строку математического выражения из списка аргументов операции."""
        if not isinstance(args, list):
            raise TypeError(f'должен быть подан list, а не {args.__class__.__name__}')
        return oper_notation.join(x.val.repres(x.trees)
                                  if isinstance(x, exprtree) else
                                  str(x) for x in args)

    return infix_parser, infix_repres

def grouping_parser_and_repres(oper_start: str, oper_end: str, oper: operation) -> ('func(str|stringolist) -> exprtree|stringolist|None', 'func(list) -> str'):
    """Возвращает функцию-парсер и функцию представления твоей операции.
oper_start - обозначение открывающей части операции в строковом выражении;
oper_end - обозначение закрывающей части операции в строковом выражении;
oper - сама операция, у которой ещё нет функций парсеровки и представления.

Аргументы oper_start, oper_end должны быть уникальными строками частей операции, которые не являются подстроками других частей своей и других операций, для правильной обработки строкового выражения.

Для создания своей операции-группы нужно:
1. Создать экземпляр операции;
2. Обновить его функции парсировки и представления с помощью этой функции.
Вот, как это выглядит в коде:
circle_qroup = operation('(x)')
circle_qroup.update_funcs(grouping_parser_and_repres('(', ')', circle_qroup))"""
    if isinstance(oper_start, str):
        oper_start = stringolist(list(oper_start))
    elif not isinstance(oper_start, stringolist):
        raise TypeError(f'первый аргумент должен быть str или stringolist, а встреченно {oper_start.__class__.__name__}')
    if isinstance(oper_end, str):
        oper_end = stringolist(list(oper_end))
    elif not isinstance(oper_end, stringolist):
        raise TypeError(f'второй аргумент должен быть str или stringolist, а встреченно {oper_end.__class__.__name__}')
    oper_start_len = len(oper_start)
    oper_end_len = len(oper_end)

    def grouping_parser(exp: 'str|stringolist') -> 'exprtree|stringolist|None':
        """Обрабатывает строку."""
        if isinstance(exp, str):
            exp = stringolist(list(exp))
        elif not isinstance(exp, stringolist):
            raise TypeError(f'ожидался str или stringolist, а встреченно {exp.__class__.__name__}')
        res = exp.copy()
        computed = False
        s_p = 0
        while True:
            s_p = res.find(oper_start, s_p)
            if s_p == -1:
                break
            e_p = pair_of(res, oper_start, oper_end, s_p)
            inner = res[s_p + oper_start_len:e_p]
            res = res[:s_p] + stringolist([exprtree(oper, [inner])]) + res[e_p + oper_end_len:]
            computed = True
        if computed:
            if len(res) == 1:
                res = res[0]
            return res
        return None

    def grouping_repres(args: list) -> str:
        """Создаёт строку математического выражения из списка аргументов операции."""
        if not isinstance(args, list):
            raise TypeError(f'должен быть подан list, а не {args.__class__.__name__}')
        if len(args) != 1:
            raise ValueError(f'операции-группы имеют только один аргумент')
        arg = args[0]
        return oper_start.to_str() + (arg.val.repres(arg.trees)
                                      if isinstance(arg, exprtree) else
                                      str(arg)) + oper_end.to_str()

    return grouping_parser, grouping_repres

def prefix_parser_and_repres(oper_prefix: str, oper: operation, group_args_seps: list = None) -> ('func(str|stringolist) -> exprtree|stringolist|None', 'func(list) -> str'):
    """Возвращает функцию-парсер и функцию представления твоей операции.
oper_prefix - обозначение префиксной части операции в строковом выражении;
oper - сама операция, у которой ещё нет функций парсеровки и представления;
group_args_seps - список пар из операций-групп и разделителей операций-групп, принимаемых в качестве аргумента (по-умолчанию: None).

Аргумент oper_prefix должен быть уникальной строкой, которая не является подстрокой других частей других операций, для правильной обработки строкового выражения.

Аргумент group_args_seps задаёт список пар операций-групп и разделителей аргументов внутри групп, к которым применяется данная операция. Если значение аргумента - None, операция применяется ко всему справа.
Элементы списка должны быть кортежами из операции-группы/None и строки/строко-списка/None. Если первый элемент кортежа None, то принимается любой следующий аргумент в строке. Если второй элемент кортежа None, то разбивка группы не требуется.
Например, операция "sum_of_root[n](x,y)" - сумма корней n-ой степени из аргументов "x" и "y" - имеет две группы аргументов "[]" и "()". Список будет иметь вид: "[(square_group, None), (circle_group, ',')]".
square_qroup = operation('[x]')
square_group.update_funcs(grouping_parser_and_repres('[', ']', square_group))
circle_qroup = operation('(x)')
circle_qroup.update_funcs(grouping_parser_and_repres('(', ')', circle_qroup))

Для создания своей префиксной операции нужно:
1. Создать экземпляр операции;
2. Обновить его функции парсировки и представления с помощью этой функции.
Вот, как это выглядит в коде:
sin = operation('sin')
sin.funcs_update(prefix_parser_and_repres('sin', sin, [None]))"""
    if isinstance(oper_prefix, str):
        oper_prefix = stringolist(list(oper_prefix))
    elif not isinstance(oper_prefix, stringolist):
        raise TypeError(f'первый аргумент должен быть str или stringolist, а встреченно {oper_prefix.__class__.__name__}')
    if not (group_args_seps is None or isinstance(group_args_seps, list)):
        raise TypeError(f'аргумент group_args_seps должен быть list или None, а не {group_args_seps.__class__.__name__}')
    oper_prefix_len = len(oper_prefix)
    group_args_seps_len = len(group_args_seps)

    if group_args_seps is None:
        def prefix_parser(exp: 'str|stringolist') -> 'exprtree|stringolist|None':
            """Обрабатывает строку."""
            if isinstance(exp, str):
                exp = stringolist(list(exp))
            elif not isinstance(exp, stringolist):
                raise TypeError(f'ожидался str или stringolist, а встреченно {exp.__class__.__name__}')
            return exprtree(oper, exp[oper_prefix_len:]) if exp.startswith(oper_prefix) else None

        def prefix_repres(args: list) -> str:
            """Создаёт строку математического выражения из списка аргументов операции."""
            if not isinstance(args, list):
                raise TypeError(f'должен быть подан list, а не {args.__class__.__name__}')
            if len(args) != 1:
                raise ValueError(f'операция {oper.name} должна иметь только один аргумент, а не {len(args)}')
            arg = args[0]
            return oper_prefix.to_str() + (arg.val.repres(arg.trees)
                                           if isinstance(arg, exprtree) else
                                           str(arg))
    else:
        def prefix_parser(exp: 'str|stringolist') -> 'exprtree|stringolist|None':
            """Обрабатывает строку."""
            if isinstance(exp, str):
                exp = stringolist(list(exp))
            elif not isinstance(exp, stringolist):
                raise TypeError(f'ожидался str или stringolist, а встреченно {exp.__class__.__name__}')
            res = exp.copy()
            computed = False
            pos = 0
            while True:
                pos = res.find(oper_prefix, pos)
                if pos == -1:
                    break
                arg_pos = pos + oper_prefix_len
                if not (arg_pos + group_args_seps_len <= len(res) and
                        all((g := group_args_seps[n][0]) is None or
                            (isinstance((a := res[arg_pos + n]), exprtree) and
                             a.val == g)
                            for n in range(group_args_seps_len))):
                    pos += 1
                    continue
                cur_obj = exprtree(oper, [[]])
                #res = res[:pos] + res[arg_pos:]
                for n, (group, sep) in enumerate(group_args_seps):
                    cur_arg = res[arg_pos + n]
                    cur_args = cur_arg.trees[0].split(sep) if isinstance(cur_arg.trees[0], stringolist) else [cur_arg.trees[0]]
                    cur_obj.trees += cur_args
                    cur_obj.trees[0].append(len(cur_args))
                res = res[:pos] + stringolist(cur_obj) + res[arg_pos + group_args_seps_len:]
                computed = True
            if computed:
                if len(res) == 1:
                    res = res[0]
                return res
            return None

        def prefix_repres(args: list) -> str:
            """Создаёт строку математического выражения из списка аргументов операции."""
            if not isinstance(args, list):
                raise TypeError(f'должен быть подан list, а не {args.__class__.__name__}')
            #args_len = len(args)
            #if not args_len == group_args_seps_len:
            #    raise ValueError(f'число аргументов операции {oper.name} должно быть {group_args_seps_len}, а не {args_len}')
            res = oper_prefix.to_str()
            k = 1
            for n, var_count in enumerate(args[0]):
                group, sep = group_args_seps[n]
                new_k = k + var_count
                vs = args[k:new_k]
                k = new_k
                if sep is None:
                    if len(vs) != 1:
                        raise RuntimeError(f'ожидалось одно значение в группе "{group.name}", а встреченно {len(vs)}')
                    res += group.repres([str(vs[0])])
                else:
                    res += group.repres(sep.join(str(x) for x in vs))
            return res

    return prefix_parser, prefix_repres

def object_parser_and_repres(is_object: 'func(stringolist) -> bool',
                             oper: operation,
                             to_object: 'func(stringolist) -> any' = None,
                             to_stringolist: 'func(any) -> stringolist' = None) -> ('func(str|stringolist) -> exprtree|stringolist|None', 'func(list) -> str'):
    """Возвращает функцию-парсер и функцию представления твоего объекта.
is_object - функция, которая проверяет правильность представления твоего объекта;
oper - сам объект, у которой ещё нет функций парсеровки и представления;
to_object - функция, которая возвращает объект из строко-списка;
to_stringolist - функция, которая возвращает представление в строко-списке вашего объекта.

Аргумент is_object должен принимать строко-список и возвращать True или False взависимости от того можно ли твой объект представить в виде поданого строко-списка.

Аргумент to_object должен быть None или функцией, которая принимает только строко-список и возвращает соответствующий ему объект.

Аргумент to_stringolist должен быть None или функцией, которая принимает только ваш объект и возвращает соответствующий ему строко-список.

Для создания своего объекта нужно:
1. Создать экземпляр операции;
2. Обновить его функции парсировки и представления с помощью этой функции.
Вот, как это выглядит в коде:
int_number = operation('int number')
sin.funcs_update(object_parser_and_repres(lambda x: x.is_str() and x.to_str().isdigit(), int_number))"""
    if not callable(is_object):
        raise TypeError(f'первый аргумент должен быть вызываемым, а не {is_object.__class__.__name__}')
    elif is_object.__code__.co_argcount != 1:
        raise ValueError(f'первый аргумент должен принимать ровно один аргумент, а не {is_object.__code__.co_argcount}')
    if to_object is None:
        to_object = lambda x: x
    if not callable(to_object):
        raise TypeError(f'to_object должен быть вызываемым, а не {to_object.__class__.__name__}')
    elif to_object.__code__.co_argcount != 1:
        raise ValueError(f'to_object должен принимать ровно один аргумент, а не {to_object.__code__.co_argcount}')
    if to_stringolist is None:
        to_stringolist = lambda x: str(x)
    if not callable(to_stringolist):
        raise TypeError(f'to_stringolist должен быть вызываемым, а не {to_stringolist.__class__.__name__}')
    elif to_stringolist.__code__.co_argcount != 1:
        raise ValueError(f'to_stringolist должен принимать ровно один аргумент, а не {to_stringolist.__code__.co_argcount}')

    def object_parser(exp: 'str|stringolist') -> 'exprtree|stringolist|None':
        """Обрабатывает строку."""
        if isinstance(exp, str):
            exp = stringolist(list(exp))
        elif not isinstance(exp, stringolist):
            raise TypeError(f'ожидался str или stringolist, а встреченно {exp.__class__.__name__}')
        if is_object(exp):
            return exprtree(oper, [to_object(exp)])
        return None

    def object_repres(args: list) -> str:
        """Создаёт строку математического выражения из списка аргументов операции."""
        if not isinstance(args, list):
            raise TypeError(f'должен быть подан list, а не {args.__class__.__name__}')
        if len(args) != 1:
            raise ValueError(f'операции-объекты имеют только один аргумент')
        return to_stringolist(args[0]).to_str()

    return object_parser, object_repres

def operInfix(oper_name: str, oper_notation) -> operation:
    """Возвращает инфиксную операцию.
oper_name - имя операции;
oper_notation - обозначение инфиксной операции в строковом выражении."""
    res = operation(oper_name)
    res.funcs_update(infix_parser_and_repres(oper_notation, res))
    return res

def operGrouping(oper_name: str, oper_start: str, oper_end: str) -> operation:
    """Возвращает инфиксную операцию.
oper_name - имя операции;
oper_start - обозначение открывающей части операции в строковом выражении;
oper_end - обозначение закрывающей части операции в строковом выражении."""
    res = operation(oper_name)
    res.funcs_update(grouping_parser_and_repres(oper_start, oper_end, res))
    return res

def operPrefix(oper_name: str, oper_prefix: str, group_args_seps: list = None) -> operation:
    """Возвращает префиксную операцию.
oper_name - имя операции;
oper_prefix - обозначение префиксной части операции в строковом выражении;
group_args_seps - список пар из операций-групп и разделителей операций-групп, принимаемых в качестве аргумента (по-умолчанию: None)."""
    res = operation(oper_name)
    res.funcs_update(prefix_parser_and_repres(oper_prefix, res, group_args_seps))
    return res

def operObject(oper_name: str,
               is_object: 'func(stringolist) -> bool',
               to_object: 'func(stringolist) -> any' = None,
               to_stringolist: 'func(any) -> stringolist' = None) -> operation:
    """Возвращает объект в виде операции.
is_object - функция, которая проверяет правильность представления твоего объекта;
to_object - функция, которая возвращает объект из строко-списка;
to_stringolist - функция, которая возвращает представление в строко-списке вашего объекта."""
    res = operation(oper_name)
    res.funcs_update(object_parser_and_repres(is_object, res, to_object, to_stringolist))
    return res


operation_reduce_without_dill = operation.__reduce__

_dill_is_imported = False
_pickle_is_imported = False

def dill_disable():
    """Отключает возможность пользоваться библиотекой "dill" для функций и методов библиотеки "pyxration"."""
    global cmp, _dumps
    operation.__reduce__ = operation_reduce_without_dill
    if _pickle_is_imported:
        cmp = _cmp_with_pickle
        _dumps = pickle.dumps
    else:
        cmp = _cmp_first_call
        _dumps = None

def dill_enable():
    """Если установлена библиотека "dill", включает возможность пользоваться ею для функций и методов библиотеки "pyxration", иначе - отключает её использование."""
    global cmp, _dumps
    if find_spec('dill') is None:
        dill_disable()
    else:
        del operation.__reduce__
        if _dill_is_imported:
            cmp = _cmp_with_dill
            _dumps = dill.dumps
        else:
            cmp = _cmp_first_call
            _dumps = None

dill_enable()

if __name__ == '__main__':
    if False:
        def plus_parser(exp: 'str|stringolist') -> 'exprtree|None':
            """Обрабатывает строку. Сначала нужно обработать строку на обособляемые операции."""
            if isinstance(exp, str):
                exp = stringolist(list(exp))
            elif not isinstance(exp, stringolist):
                raise TypeError(f'Ожидался str или stringolist, а встреченно {exp.__class__.__name__}')
            args = exp.split(stringolist(['+']))
            return exprtree(plus_operation, args) if len(args) > 1 else None

        def plus_repres(args: list) -> str:
            """Создаёт строку математического выражения из списка аргументов операции "+"."""
            return '+'.join(str(x) for x in args)

        plus_operation = operation('addition', plus_parser, plus_repres)

        expr = 'x+y+z+w'
        processed_expr = plus_operation.parser(expr)
        print(expr, processed_expr, sep = '\n')

        mul_operation = operation('multiplication')
        mul_operation.funcs_update(infix_parser_and_repres('*', mul_operation))
        expr = 'x*y*z*w'
        processed_expr = mul_operation.parser(expr)
        print(expr, processed_expr, sep = '\n')
    if False:
        expr = 'x+(y*z+(w-x*y)/z)*w'
        expr_sl = stringolist(list(expr))
        o_p = stringolist('(')
        c_p = stringolist(')')
        o_p_pos = expr_sl.find(o_p)
        fake_c_p_pos = expr_sl.find(c_p) #Найдёт первую попавшуюся ")".
        c_p_pos = pair_of(expr_sl, o_p, c_p, o_p_pos) #Найдёт парную закрывающую часть ")".
        print(f'{expr = }')
        print(f'{fake_c_p_pos = }, {c_p_pos = }')
    if False:
        dot_product = operation('dot product')
        dot_product.funcs_update(outfix_parser_and_repres('(', ')', ',', dot_product))
        expr = 'r+(r,g)-((q,w),e)'
        processed_expr = dot_product.parser(expr)
        print(expr, processed_expr, sep = '\n')
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
        simple = algebra('simple',
                         [x for x in group.values()] + [split, plus, minus, power, sin, cos, root, int_num, variable],
                         [int_num, variable, sin, cos, root, power, plus, minus, split] + [x for x in group.values()],
                         group['()'])
        expr = 'sin(root[2](x))^2+cos(root[2](x))^2+[({r,q},e)-root[n](78)]'
        exps = stringolist(list(expr))
        expt = simple.new_expr(exps)
        expt1 = simple.new_expr(exps)
        simple.order_brackets_del(expt1)
        print(expr, str_tree(expt), sep = ':\n')
        print('expr =', simple.to_str(expr))
        print(f'{simple.order_brackets_del(expt) = }')
        print(expr, str_tree(expt), sep = ':\n')
        print('expr =', simple.to_str(expr))
        print(f'{expr}\n==\n{expr}\n=\n{expt == expt1}')
    if False:
        a = 'a'
        b = 1
        print(f'a = {a!r}\nb = {b!r}\n\t{cmp(a, b) = }\n\t{cmp(b, a) = }')
        a = operation('oper')
        b = operation('oper')
        print(f'a = {a!r}\nb = {b!r}\n\t{cmp(a, b) = }\n\t{cmp(b, a) = }')
        b.funcs_update(infix_parser_and_repres('+', b))
        print(f'a = {a!r}\nb = {b!r}\n\t{cmp(a, b) = }\n\t{cmp(b, a) = }')
        a = ['a']
        b = [1]
        print(f'a = {a!r}\nb = {b!r}\n\t{cmp(a, b) = }\n\t{cmp(b, a) = }')
