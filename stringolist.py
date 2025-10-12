class stringolist:
    """Класс строки с объектами вместо символов."""

    def __init__(self, *args):
        args_len = len(args)
        if args_len == 0:
            self.val = []
        elif args_len == 1:
            self.val = args[0] if isinstance(args[0], list) else [args[0]]
        else:
            self.val = args

    def __eq__(self, other):
        return isinstance(other, stringolist) and self.val == other.val

    def __ne__(self, other):
        return not isinstance(other, stringolist) or self.val != other.val

    def __add__(self, other):
        if isinstance(other, stringolist):
            return stringolist(self.val + other.val)
        raise TypeError(f"unsupported operand type(s) for +: '{self.__class__.__name__}' and '{other.__class__.__name__}'")

    def __iadd__(self, other):
        if isinstance(other, stringolist):
            self.val += other.val
            return self
        raise TypeError(f"unsupported operand type(s) for +=: '{self.__class__.__name__}' and '{other.__class__.__name__}'")

    def __mul__(self, other):
        return stringolist(self.val * other)

    def __rmul__(self, other):
        return self * other

    def __imul__(self, other):
        self.val *= other
        return self

    def __str__(self):
        return str(self.val)

    def __repr__(self):
        return f'stringolist([{", ".join(repr(x) for x in self.val)}])'

    def __bool__(self):
        return bool(self.val)

    def __len__(self):
        return len(self.val)

    def __getitem__(self, key: int):
        try:
            if isinstance(key, int):
                return self.val[key]
            elif isinstance(key, slice):
                return stringolist(self.val[key])
            else:
                raise TypeError(f"stringolist indices must be integers or slices, not {key.__class__.__name__}")
        except IndexError:
            raise IndexError("stringolist index out of range") from None

    def __iter__(self):
        for x in self.val:
            yield x

    def __reversed__(self):
        return reversed(self.val)

    def __contains__(self, item):
        if isinstance(item, stringolist):
            self_len = len(self)
            item_len = len(item)
            if item_len == 0:
                return True
            elif self_len < item_len:
                return False
            for i in range(self_len - item_len + 1):
                found = True
                for j in range(item_len):
                    found = self[i + j] == item[j]
                    if not found:
                        break
                if found:
                    return True
            return False
        raise TypeError(f"must be stringolist, not {item.__class__.__name__}")

    def copy(self):
        return stringolist(self.val.copy())

    def deepcopy(self):
        new_list = []
        for x in self.val:
            try:
                new_list.append(x.deepcopy())
            except AttributeError:
                new_list.append(x)
        return stringolist(new_list)

    def append(self, object):
        """Appends object to the end of the stringolist."""
        self.val.append(object)

    def find(self, sub, start: int = 0, stop: int = None):
        """Finds substringolist from current stringolist and returns index of first enter of sub.
If sub is not substringolist of current stringolist then return -1."""
        s = slice(start, stop)
        self_len = len(self)
        start_norm, stop_norm, _ = s.indices(self_len)
        if isinstance(sub, stringolist):
            self_slice_len = stop_norm - start_norm
            sub_len = len(sub)
            last_start_index = stop_norm - sub_len
            if sub_len == 0: #Пустая подстрока есть в любой строке
                return start_norm
            elif (self_slice_len < sub_len or #Срез меньше искомой подстроки
                  start_norm > last_start_index):# or #Последнее возможное начало подстроки находится левее среза
                  #start_norm >= stop_norm): #Срез является нулевым или отрицательным (лишняя проверка потому что в первой проверке sub_len гарантированно больше 0, пока закомментирую)
                return -1
            for i in range(start_norm, last_start_index + 1):
                found = True
                for j in range(sub_len):
                    found = self[i + j] == sub[j]
                    if not found:
                        break
                if found:
                    return i
            return -1
        raise TypeError(f"must be stringolist, not {sub.__class__.__name__}")

    def rfind(self, sub, start: int = 0, stop: int = None):
        """Finds substringolist from current stringolist and returns index of last enter of sub.
If sub is not substringolist of current stringolist then return -1."""
        s = slice(start, stop)
        self_len = len(self)
        start_norm, stop_norm, _ = s.indices(self_len)
        if isinstance(sub, stringolist):
            self_slice_len = stop_norm - start_norm
            sub_len = len(sub)
            last_start_index = stop_norm - sub_len
            if sub_len == 0: #Пустая подстрока есть в любой строке
                return start_norm
            elif (self_slice_len < sub_len or #Срез меньше искомой подстроки
                  last_start_index < start_norm):# or #Последнее возможное начало подстроки находится левее среза
                  #start_norm >= stop_norm): #Срез является нулевым или отрицательным (лишняя проверка потому что в первой проверке sub_len гарантированно больше 0, пока закомментирую)
                return -1
            for i in range(last_start_index, start_norm - 1, -1):
                found = True
                for j in range(sub_len):
                    found = self[i + j] == sub[j]
                    if not found:
                        break
                if found:
                    return i
            return -1
        raise TypeError(f"must be stringolist, not {sub.__class__.__name__}")

    def index(self, value, start: int = 0, stop: int = None):
        """Returns first index of value in stringolist.
If value is not in current stringolist then returns -1."""
        return self.val.index(value, start, stop)

    def replace(self, old, new, count: int = -1):
        """Return a copy with all occurrences of substring old replaced by new.
count - maximum number of occurrences to replace.
-1 (the default value) means replace all occurrences.
If the optional argument count is given, only the first count occurrences are replaced."""
        if not isinstance(old, stringolist):
            raise TypeError(f'replace() argument 1 must be stringolist, not {old.__class__.__name__}')
        if not isinstance(new, stringolist):
            raise TypeError(f'replace() argument 2 must be stringolist, not {new.__class__.__name__}')
        if not isinstance(count, int):
            raise TypeError(f'\'{count.__class__.__name__}\' object cannot be interpreted as an integer')
        res = stringolist()
        k = 0
        self_len = len(self)
        old_len = len(old)
        #new_len = len(new)
        last_start_index = self_len - old_len
        while k < self_len:
            if k > last_start_index:
                res += self[k:]
                break
            found = True
            for i in range(old_len):
                found = self[k + i] == old[i]
                if not found:
                    break
            if found and count:
                res += new
                k += old_len
                count -= 1
            else:
                res.append(self[k])
                k += 1
        return res

    def split(self, sep = None, maxsplit = -1):
        """Return a list of the substringolists in the stringolist, using sep as the separator stringolist.
sep - the separator used to split the stringolist.
When set to None (the default value), will split on any whitespace character
(including stringolist('\\n'), stringolist('\\r'), stringolist('\\t'), stringolist('\\f') and spaces) and will discard empty strings from the result.
maxsplit - maximum number of splits.
-1 (the default value) means no limit.
Splitting starts at the front of the string and works to the end.
Note, str.split() is mainly useful for data that has been intentionally delimited.
With natural text that includes punctuation, consider using the regular expression module."""
        if not isinstance(sep, (type(None), stringolist)):
            raise TypeError(f'must be stringolist or None, not {sep.__class__.__name__}')
        if not isinstance(maxsplit, int):
            raise TypeError(f'\'{maxsplit.__class__.__name__}\' object cannot be interpreted as an integer')
        res = []
        if sep is None:
            whitespace = {'\n', '\r', '\t', '\f', ' '}
            token = stringolist()
            for obj in self.val:
                if maxsplit and obj in whitespace:
                    res.append(token)
                    token = stringolist()
                else:
                    if maxsplit:
                        maxsplit -= 1
                    token.append(obj)
            res.append(token)
            return res
        k = 0
        self_len = len(self)
        sep_len = len(sep)
        last_start_index = self_len - sep_len
        token = stringolist()
        while k < self_len:
            if k > last_start_index:
                token += self[k:]
                break
            found = True
            for i in range(sep_len):
                found = self[k + i] == sep[i]
                if not found:
                    break
            if found and maxsplit:
                res.append(token)
                token = stringolist()
                k += sep_len
                maxsplit -= 1
            else:
                token.append(self[k])
                k += 1
        res.append(token)
        return res

    def startswith(self, prefix, start: int = 0, end: int = None) -> bool:
        """S.startswith(prefix[, start[, end]]) -> bool
Return True if S starts with the specified prefix, False otherwise.
With optional start, test S beginning at that position.
With optional end, stop comparing S at that position.
prefix can also be a tuple of stringolists to try."""
        if isinstance(prefix, stringolist):
            s = slice(start, end)
            self_len = len(self)
            prefix_len = len(prefix)
            start_norm, stop_norm, step_norm = s.indices(self_len)
            self_slice_len = stop_norm - start_norm
            last_start_index = stop_norm - prefix_len
            if prefix_len == 0:
                return True
            elif (self_slice_len < prefix_len or
                  last_start_index < start_norm):
                return False
            for i in range(prefix_len):
                if self[start_norm + i] == prefix[i]:
                    return True
            return False
        elif isinstance(prefix, tuple):
            for obj in prefix:
                if isinstance(obj, stringolist):
                    if self.startswith(obj, start, end):
                        return True
                else:
                    TypeError(f'tuple for startswith must only contain stringolist, not {obj.__class__.__name__}')
            return False
        else:
            raise TypeError(f'startswith first arg must be stringolist or a tuple of stringolist, not {prefix.__class__.__name__}')

    def endswith(self, suffix, start: int = 0, end: int = None) -> bool:
        """S.endswith(suffix[, start[, end]]) -> bool
Return True if S ends with the specified suffix, False otherwise.
With optional start, test S beginning at that position.
With optional end, stop comparing S at that position.
suffix can also be a tuple of stringolists to try."""
        if isinstance(suffix, stringolist):
            s = slice(start, end)
            self_len = len(self)
            suffix_len = len(suffix)
            start_norm, stop_norm, step_norm = s.indices(self_len)
            self_slice_len = stop_norm - start_norm
            last_start_index = stop_norm - suffix_len
            if suffix_len == 0:
                return True
            elif (self_slice_len < suffix_len or
                  last_start_index < start_norm):
                return False
            for i in range(suffix_len):
                if self[last_start_index + i] == suffix[i]:
                    return True
            return False
        elif isinstance(suffix, tuple):
            for obj in suffix:
                if isinstance(obj, stringolist):
                    if self.endswith(obj, start, end):
                        return True
                else:
                    TypeError(f'tuple for endswith must only contain stringolist, not {obj.__class__.__name__}')
            return False
        else:
            raise TypeError(f'endswith first arg must be stringolist or a tuple of stringolist, not {suffix.__class__.__name__}')

    def is_str(self):
        """Return True if the stringolist is a stringolist of strings, False otherwise.
A stringolist is a stringolist of strings if all elements in the stringolist are strings."""
        return all([isinstance(x, str) for x in self.val])

    def to_str(self):
        """Convert stringolist to string if all elements are strings.
Raises TypeError if any element is not a string."""
        try:
            return ''.join(self.val)
        except TypeError as e:
            for i, item in enumerate(self.val):
                if not isinstance(item, str):
                    raise TypeError(f"stringolist elements must be str, not {type(item).__name__} "
                                    f"at index {i}") from None
            raise  # На всякий случай, если ошибка по другой причине

if __name__ == '__main__':
    digits = stringolist(list(range(10)))
    d345 = stringolist(list(range(3, 6)))
    print(f'{digits = }')
    print(f'{d345 = }')
    print(f'{digits.find(d345) = }')
    print(f'{digits.find(d345, 3) = }')
    print(f'{digits.find(d345, 4) = }')
    print(f'{digits.find(d345, 3, 5) = }')
    print(f'{digits.find(d345, 3, 6) = }')
    palindrome = stringolist(list((a := 'coconut')) + list(reversed(a[:-1])))
    oco = stringolist(list('oco'))
    print(f'{palindrome = }')
    print(f'{oco = }')
    print(f'{palindrome.find(oco) = }')
    print(f'{palindrome.rfind(oco) = }')
    print(f'{palindrome.rfind(oco, 0, 7) = }')
    print(f'{palindrome.rfind(oco, 7) = }')
    print(f'{palindrome.rfind(oco, 0, 11) = }')
    print(f'{palindrome.rfind(oco, 0, 12) = }')

    xxxx = stringolist(list('xxxx'))
    xx = stringolist(list('xx'))
    x = stringolist(list('x'))
    print(*[f'{obj = }' for obj in [xxxx, xx, x]], sep = '\n')
    print(f'{xxxx.replace(xx, x) = }')
    print(f'{xxxx.replace(xx, x, 1) = }')
    x_x_x_x = stringolist(list('x_x_x_x'))
    x_x = stringolist(list('x_x'))
    _ = stringolist('_')
    x_whitespaces = stringolist(list('x\nx\rx\tx\fx x'))
    print(*[f'{obj = }' for obj in [x_x_x_x, x_x, _, x_whitespaces]], sep = '\n')
    print(f'{xxxx.split(x) = }')
    print(f'{x_x_x_x.split(_) = }')
    print(f'{x_x_x_x.split(_, 2) = }')
    print(f'{x_x_x_x.split(x_x) = }')
    print(f'{x_x_x_x.split(x_x, 1) = }')
    print(f'{x_whitespaces.split() = }')
    print(f'{x_whitespaces.split(None, 2) = }')

    print('\n', *[f'{obj!r}.is_str = {obj.is_str()}' for obj in [digits, d345, palindrome, oco, xxxx, xx, x, x_x_x_x, x_x, _, x_whitespaces]], sep = '\n')
    
    print('\n', *[f'{obj!r}.to_str() = {obj.to_str()!r}' for obj in [digits, d345, palindrome, oco, xxxx, xx, x, x_x_x_x, x_x, _, x_whitespaces] if obj.is_str()], sep = '\n')
