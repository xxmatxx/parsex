from parsex.parsex import sepBy,between, string, lazy, choice, digits

betweenSquareBrackets = between(string("["),string("]"))
commaSeparator = sepBy(string(","))

def valueThunk():  return value

valueParser = lazy(valueThunk)

arrayParser = betweenSquareBrackets(commaSeparator(valueParser))

value = choice([
    digits,
    arrayParser
])


print(arrayParser.run("[1,2,3,[1,2,3,[]]]"))