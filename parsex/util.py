def updateParserState(state, index, result):
    newState = state.copy()
    newState["result"] = result
    newState["index"] = index
    return newState

def updateParserResult(state, result):
    newState = state.copy()
    newState["result"] = result
    return newState

def updateParserError(state, errorMsg):
    newState = state.copy()
    newState["error"] = errorMsg
    newState["isError"] = True
    return newState

class Parser():
    def __init__(self, parserStateTransformerFn):
        self.parserStateTransformerFn = parserStateTransformerFn

    def run(self, targetString):
        initialState = {
            "targetString": targetString,
            "index": 0,
            "result": None,
            "isError": False,
            "error": None
        }
        return self.parserStateTransformerFn(initialState)

    def map(self, fn):
        def fn1 (parserState):
            nextState = self.parserStateTransformerFn(parserState)

            if nextState["isError"]:
                return nextState

            return updateParserResult(nextState,fn(nextState["result"]))
        return Parser(fn1)

    def chain(self, fn):
        def fn1 (parserState):
            nextState = self.parserStateTransformerFn(parserState)

            if nextState["isError"]:
                return nextState

            nextParser = fn(nextState["result"])
            return nextParser.parserStateTransformerFn(nextState)
        return Parser(fn1)


    def errorMap(self, fn):
        def fn1 (parserState):
            nextState = self.parserStateTransformerFn(parserState)

            if not nextState["isError"]:
                return nextState

            return updateParserError(nextState,fn(nextState["error"]))
        return Parser(fn1)