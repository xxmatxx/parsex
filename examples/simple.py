from parsex.parsex import sequenceOf,string,choice,many,many1, between,letters,digits,sepBy,sepBy1

print(sequenceOf([string("hello"),string("wolrd"),string("!")]).run("hello wolrd!"))

print(string("hello").map(lambda a: a.upper()).run("hello"))
print(string("hellob").map(lambda a: a.upper()).run("helloa"))

print(choice([string("133"),string("111")]).run("sas"))

print(many(string("1")).run("111222"))
print(many(string("1")).run("222"))
print(many1(string("1")).run("111222"))
print(many1(string("1")).run("222"))

print(between(string("("), string(")"))(string("hello")).run("(hello)"))

test = sequenceOf([string("("), string("hello"), string(")") ])
print(test.run("(hello)"))

print(letters.run("sad564"))
print(letters.run("564sad564"))

print(digits.run("sad564"))
print(digits.run("564sad564"))

print(sepBy(string(","))(letters).run("sd,ds,456,dssds"))
print(sepBy(string(","))(letters).run("sd,ds,dsd,dssds"))

print(sepBy1(string(","))(letters).run("sd,ds,456,dssds"))
print(sepBy1(string(","))(letters).run("sd,ds,dsd,dssds"))
print(sepBy1(string(","))(letters).run("11,ds,dsd,dssds"))