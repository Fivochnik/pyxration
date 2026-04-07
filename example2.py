import pyxpration as pyx
from pyxpration import transtree as pyxt

bracket = pyx.operGrouping('()', '(', ')')
quad = pyx.operGrouping('[]', '[', ']')
comma = pyx.operInfix('comma', ',')
plus = pyx.operInfix('plus', '+')
mul = pyx.operInfix('mul', '*')

sin = pyx.operPrefix('sin', 'sin', [(bracket, None)])

func = pyx.operPrefix('function', 'func', [(quad, None), (bracket, ',')])

var = pyx.operObject('var',
                     lambda x: x.is_str() and x.to_str().isidentifier(),
                     lambda x: x.to_str(),
                     lambda x: pyx.stringolist(list(x)))

alg = pyx.algebra('algebra',
                  [bracket, quad, sin, func, comma, plus, mul, var],
                  [bracket, quad, var, sin, func, mul, plus, comma],
                  bracket)

func_1 = alg.new_func('%x%+sin(%y%)*func[MyFunc](a,b)', [pyx.funcparam('x'), pyx.funcparam('y')])

print(alg.to_str(func_1), pyx.str_tree(func_1), sep = '\n')
