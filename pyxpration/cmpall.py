cmp = _dumps = None

def _cmp_start(a: object, b: object) -> 'int|None':
    """Сравнивает пару объектов на некотором линейном строгом порядке.
Возвращает -1, если a < b. 1, если a > b. 0, если a is b. Иначе - None."""
    if a is b:
        return 0
    type_a = type(a)
    type_b = type(b)
    type_a_name = type_a.__name__
    type_b_name = type_b.__name__
    if type_a_name != type_b_name:
        return -1 if type_a_name < type_b_name else 1

def _cmp_with_dill(a: object, b: object) -> int:
    """Сравнивает пару объектов на некотором линейном строгом порядке.
Возвращает -1, если a < b. 1, если a > b. Иначе - 0."""
    _cmps = _cmp_start(a, b)
    if not _cmps is None:
        return _cmps
    type_a = type(a)
    type_b = type(b)
    if type_a != type_b:
        return _cmp_with_dill(type_a, type_b)
    dumps_a = _dumps(a)
    dumps_b = _dumps(b)
    if dumps_a == dumps_b:
        return 0
    return -1 if dumps_a < dumps_b else 1

def _cmp_with_pickle(a: object, b: object) -> int:
    """Сравнивает пару объектов на некотором линейном строгом порядке.
Возвращает -1, если a < b. 1, если a > b. 0, если a == b. None, если есть сомнения."""
    _cmps = _cmp_start(a, b)
    if not _cmps is None:
        return _cmps
    type_a = type(a)
    type_b = type(b)
    if type_a != type_b:
        return _cmp_with_pickle(type_a, type_b)
    try:
        dumps_a = _dumps(a)
        dumps_b = _dumps(b)
    except:
        return
    if dumps_a == dumps_b:
        return 0
    return -1 if dumps_a < dumps_b else 1

def _cmp_first_call(a: object, b: object) -> int:
    """Сравнивает пару объектов на некотором линейном строгом порядке.
Возвращает -1, если a < b. 1, если a > b. 0, если a == b. None, если не установлена библиотека "dill" и есть сомнения.

Для всегда точного ответа необходимо установить библиотеку "dill"."""
    _cmps = _cmp_start(a, b)
    if not _cmps is None:
        return _cmps
    global cmp, _dumps, _dill_is_imported, _pickle_is_imported
    try:
        import dill
        _dill_is_imported = True
        cmp = _cmp_with_dill
        _dumps = dill.dumps
    except:
        import pickle
        _pickle_is_imported = True
        cmp = _cmp_with_pickle
        _dumps = pickle.dumps
    return cmp(a, b)

cmp = _cmp_first_call
