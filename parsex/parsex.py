import re
from parsex.util import Parser, updateParserState, updateParserResult, updateParserError

def lazy(parserThunk):
    """Enable define parser in recursive way.
    
    Args:
        parserThunk: Function whitch return parser.
    Returns:
        Return parser.
    """
    def fn(parserState):
        parser = parserThunk()
        return parser.parserStateTransformerFn(parserState)
    return Parser(fn)

def string(s):
    def fn (parserState):
        if parserState["isError"] == True:
            return parserState
            
        
        targetString = parserState["targetString"]
        index = parserState["index"]

        if targetString[index:].startswith(s):
            return updateParserState(parserState,index + len(s),s)
        else:
            error = "string: Tried to match %s, but got %s"%(s,targetString) 
            return updateParserError(parserState, error)
    return Parser(fn)

def match(regex):
    def fn (parserState):
        if parserState["isError"] == True:
            return parserState
            
        targetString = parserState["targetString"]
        index = parserState["index"]

        obj = re.match(regex, targetString[index:])
        if obj.span()[0] != obj.span()[1]:
            return updateParserState(parserState,index + obj.span()[1],obj.group())
        else:
            error = "match: Tried to match %s, but got %s"%(regex, targetString[index:])
            return updateParserError(parserState, error)
    return Parser(fn)

def sequenceOf(parsers):
    def fn(parserState):

        if parserState["isError"]== True:
            return parserState

        results = []
        
        nextState = parserState.copy()

        for p in parsers:
            nextState = p.parserStateTransformerFn(nextState)
            if nextState["isError"] == True:
                break
            results.append(nextState["result"])

        return updateParserResult(nextState, tuple(results))
    return Parser(fn)

def choice(parsers):
    def fn(parserState):

        if parserState["isError"]== True:
            return parserState

        for p in parsers:
            nextState = p.parserStateTransformerFn(parserState)
            if nextState["isError"] == False:
                return nextState

        error = "choice: Unable to match with any parser at index %i"%(parserState["index"]) 
        return updateParserError(nextState,error)
    return Parser(fn)

def many(parser):
    def fn(parserState):

        if parserState["isError"]== True:
            return parserState
        nextState = testState = parserState.copy()
        results = []
        done = False
        while(not done):
            testState =  parser.parserStateTransformerFn(testState)
            if not testState["isError"]:
                results.append(testState["result"])
                nextState = testState
            else:
                done = True

        return updateParserResult(nextState, tuple(results))
    return Parser(fn)

def many1(parser):
    def fn(parserState):

        if parserState["isError"]== True:
            return parserState
        nextState = testState = parserState.copy()
        results = []
        done = False
        while(not done):
            testState =  parser.parserStateTransformerFn(testState)
            if not testState["isError"]:
                results.append(testState["result"])
                nextState = testState
            else:
                done = True
        if len(results) < 1:
            return updateParserError(nextState, "many1: Unable to match any input using parser at index %i"%(parserState["index"]))   
        return updateParserResult(nextState, tuple(results))

    return Parser(fn)

def between(leftParser, rightParser):
    def fn(contentParser):
        return sequenceOf([
                leftParser,
                contentParser,
                rightParser
                ]).map(lambda results: results[1])
    return fn

def sepBy(separatorParser):
    def fn(valueParser):
        def fn1(parserState):
            results = []
            nextState = parserState.copy()

            while(True):
                thingWeWantState = valueParser.parserStateTransformerFn(nextState)
                if thingWeWantState["isError"]:
                    break
                results.append(thingWeWantState["result"])
                nextState = thingWeWantState

                separatorState = separatorParser.parserStateTransformerFn(nextState)
                if separatorState["isError"]:
                    break
                nextState = separatorState

            return updateParserResult(nextState,results)
        return Parser(fn1)
    return fn

def sepBy1(separatorParser):
    def fn(valueParser):
        def fn1(parserState):
            results = []
            nextState = parserState.copy()

            while(True):
                thingWeWantState = valueParser.parserStateTransformerFn(nextState)
                if thingWeWantState["isError"]:
                    break
                results.append(thingWeWantState["result"])
                nextState = thingWeWantState

                separatorState = separatorParser.parserStateTransformerFn(nextState)
                if separatorState["isError"]:
                    break
                nextState = separatorState
            
            if len(results) < 1:
                return updateParserError(nextState, "sepBy1: Unable to match any input using parser at index %i"%(parserState["index"]))   
            return updateParserResult(nextState, tuple(results))
        return Parser(fn1)
    return fn


letters = match(r"^[A-Za-z]*")
digits = match(r"^[0-9]*")
