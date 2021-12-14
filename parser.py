from sqlparse.tokens import Name, Punctuation, Text, Keyword, Wildcard
import sqlparse
import queue

def parser(sql):
    parsed = (sqlparse.parse(sql)[0].flatten())
    tables = []
    identifier = set()
    fields = {}
    table_alias = {}
    join_words = ("FROM", "JOIN", "INNER JOIN", "LEFT JOIN", "UNION")
    stack = queue.LifoQueue()
    state = 0
    for token in parsed:
        if token.ttype is Text.Whitespace or token.ttype is Text.Whitespace.Newline:
            continue
        # print("%s %s %s" % (token.value, state, token.ttype))
        if token.ttype is Keyword:
            if join_words.__contains__(token.value.upper()):
                state = 1
                continue
            elif iequal(token.value, 'AS'):
                if state == 2:
                    continue
            elif iequal(token.value, 'USING'):
                state = 5
                continue
            else:
                state = 0
                continue
        if token.ttype is Punctuation:
            if token.value == ',':
                if state == 2:
                    state = 1
                    continue
            if token.value == '.':
                state = 4
                continue
        if token.ttype is Wildcard:
            if state == 4:
                table_name = stack.get()
                identifier.remove(table_name)
                if table_name not in fields:
                    fields[table_name] = set()
                fields[table_name].add(token.value)
                state = 0
                continue
            else:
                stack.put(token.value)
                identifier.add(token.value)
                continue
        if token.ttype is Name:
            if state == 1:
                tables.append(token.value)
                stack.put(token.value)
                state = 2
                continue
            elif state == 2:
                table_alias[stack.get()] = token.value
                state == 1
                continue
            elif state == 4:
                table_name = stack.get()
                identifier.remove(table_name)
                if table_name not in fields:
                    fields[table_name] = set()
                fields[table_name].add(token.value)
                state = 0
                continue
            elif state == 5:
                fields[tables[-1]].add(token.value)
                fields[tables[-2]].add(token.value)
                state = 0
                continue
            else: 
                stack.put(token.value)
                identifier.add(token.value)
                continue

    for real_name in table_alias:
        alias_name = table_alias[real_name]
        if alias_name in fields: 
            rel = fields.pop(alias_name)
            if real_name in fields:
                fields[real_name] = fields[alias_name].union(rel)
            else:
                fields[real_name] = rel

    for real_name in fields:
        fields[real_name] = toList(fields[real_name])

    print(tables)
    print(table_alias)
    print(fields)
    print(identifier)

    return (toList(set(tables)), fields, toList(identifier))

def toList(s):
    return sorted(list(s))

def iequal(a, b):
    try:
        return a.upper() == b.upper()
    except AttributeError:
        return a == b
