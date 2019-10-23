from parsex.parsex import letters, digits, string, sequenceOf

stringParser = letters.map(lambda results: {"type":"number", "value":results})
numberParser = digits.map(lambda results: {"type":"number", "value":int(results)})

def mapDicerollParser(results):
    return{
        "type":"diceroll",
        "value":[int(results[0]), int(results[2])]
    }

dicerollParser = sequenceOf([
    digits,
    string("d"),
    digits
]).map(mapDicerollParser)

def choseType(type):
    if type == "string":
        return stringParser
    elif type == "number":
        return numberParser
    elif type == "diceroll":
        return dicerollParser

parser = sequenceOf([letters,string(":")
            ]).map(lambda results: results[0]
            ).chain(choseType)

print(parser.run("diceroll:5d8"))
print(parser.run("string:564"))
print(parser.run("number:5656"))