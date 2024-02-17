'''
froyo.py

Colin McBride
2/9/24
Interpreted Language Assignment 
Programming Languages

Interpreter for the FroYo language. 
'''
import sys
from collections import deque


'''
GLOBALS
'''
_vanilla = deque()
_chocolate = deque()
_cone = deque()

'''
EXTRACT PROGRAM FROM FILE
Finds the first CLOCKIN/CLOCKOUT block in the program and removes the rest. 
The CLOCKIN and CLOCKOUT lines are also removed. 
'''
def extractProgram(lines:list[str]):
    # Find beginning
    while lines[0].strip() != "CLOCKIN":
        lines.pop(0)
        if len(lines) == 0:
            raise Exception("Parse error. No CLOCKIN.")
    # end while
    lines.pop(0)

    # Find end
    for i in range(len(lines)):
        # Strip whitespace
        lines[i] = lines[i].strip()
        # Look for CLOCKOUT
        if lines[i] == "CLOCKOUT":
            break
        # end if lines[i]
    # end for i
    
    # Check if program was successfully extracted
    if lines[i] != "CLOCKOUT":
        raise Exception("Parse error. No CLOCKOUT.")
    
    # Remove all portions after CLOCKOUT
    lines = lines[:i]

    # Return parsed program
    return lines
# end extractProgram


'''
PARSE FUNCTIONS
'''
def parse(expr:str, repl:bool=False):
    # Do nothing with an empty string
    if expr == "":
        return

    # Parse expression components
    exprList = expr.split()

    # Look for string literals
    openQuote = False
    startIndex = None
    for i in range(len(exprList)):
        if exprList[i][0] == "\"" and not openQuote:
            openQuote = True
            startIndex = i
        if exprList[i][-1] == "\"" and openQuote:
            openQuote = False
            if i != startIndex:
                for j in range(startIndex+1, i+1):
                    exprList[startIndex] += " " + exprList[j]
                for j in range(startIndex, i):
                    exprList.pop(startIndex + 1)

    # Evaluate
    return evaluate(exprList, repl)
# end parse


'''
EVALUATION FUNCTION
'''
def evaluate(exprList:list[str], repl:bool=False, hold:bool=False, returnToContainer:bool=True):
    # Check if line is a comment
    if exprList[0][0] == "#":
        return
    
    # Check for loops and conditionals
    try:
        loopIndex = exprList.index("X")
    except ValueError:
        loopIndex = -1
    try:
        condIndex = exprList.index("?")
    except ValueError:
        condIndex = -1
    
    # Determine which index comes first and apply
    if (loopIndex != -1) and ((condIndex == -1) or (loopIndex < condIndex)):
        # Parse loop number as integer
        rng = evaluate(exprList[0:loopIndex], hold=hold, returnToContainer=False)
        if type(rng) != int:
            try:
                rng = int(rng)
            except Exception:
                raise Exception(f"Loop argument \"{rng}\" must be an integer")

        # Execute loop for specified number of times
        for i in range(rng):
            evaluate(exprList[(loopIndex + 1):], repl=repl)
    elif (condIndex != -1) and ((loopIndex == -1) or (condIndex < loopIndex)):
        # Only parse the rest of the expression if condition is greater than 0
        if evaluate(exprList[0:condIndex], returnToContainer=False):
            evaluate(exprList[(condIndex + 1):], repl=repl)
    else:
        # No loop or conditional; evaluate single instruction
        result = None
        dest = None
        match exprList[0]:
            case "CLOCKIN":
                if repl:
                    print("CLOCKIN has no effect in REPL mode.")
            case "CLOCKOUT":
                pass
            case "SCOOP":
                flavor = getFlavor(exprList[1])
                result = flavor[-1] if hold else flavor.pop() # was _cone.append
                dest = _cone
            case "POUR":
                flavor = getFlavor(exprList[1])
                result = flavor[0] if hold else flavor.popleft() # was _cone.append
                dest = _cone
            case "SPILL":
                if not hold:
                    flavor = getFlavor(exprList[1])
                    flavor.popleft()
            case "REFILL":
                flavor = getFlavor(exprList[1])
                result = evaluate(exprList[2:], returnToContainer=False) # was flavor.append
                dest = flavor
            case "OOPS":
                flavor = getFlavor(exprList[1])
                result = _cone[-1] if hold else _cone.pop() # was flavor.append
                dest = flavor
            case "SWIRL":
                if len(exprList) > 1:
                    result = swirl(_vanilla, _chocolate, exprList[1]) # was _cone.append
                else:
                    result = swirl(_vanilla, _chocolate, "+") # was _cone.append
                dest = _cone
            case "LRIWS":
                if len(exprList) > 1:
                    result = swirl(_chocolate, _vanilla, exprList[1]) # was _cone.append
                else:
                    result = swirl(_chocolate, _vanilla, "+") # was _cone.append
                dest = _cone
            case "HOWMUCH":
                match exprList[1]:
                    case "VANILLA":
                        result = len(_vanilla) # was _cone.append
                    case "CHOCOLATE":
                        result = len(_chocolate) # was _cone.append 
                    case "CONE":
                        result = len(_cone) # was _cone.append 
                    case _:
                        raise Exception(f"Invalid HOWMUCH container {exprList[1]}")
                dest = _cone
            case "STIR":
                flavor = getFlavor(exprList[1])
                flavor.reverse()
            case "ORDER":
                flavor = getFlavor(exprList[1])
                ipt = input()
                val, valType = getLiteral(ipt)
                if valType == int:
                    result = int(ipt) # was flavor.append
                elif valType == float:
                    result = float(ipt) # was flavor.append
                else:
                    result = ipt # was flavor.extend
                dest = flavor
            case "SERVE":
                while len(_cone) > 0:
                    print(_cone.pop(), end="")
                print()
            case "HOLD":
                result = evaluate(exprList[1:], repl=repl, hold=True, returnToContainer=returnToContainer)
            case _:
                val, valType = getLiteral(exprList[0])
                if valType != str:
                    result = val
                else:
                    val = val.split("\"")
                    if len(val) == 1:
                        raise Exception(f"Invalid command \"{exprList[0]}\"")
                    elif len(val) != 3:
                        raise Exception(f"Mismatched string quotes: {exprList[0]}")
                    else:
                        if val[0] != "" or val[2] != "":
                            raise Exception(f"Invalid string: {exprList[0]}")
                        else:
                            result = val[1]
        # end match exprList[0]
                            
        # Do things with the result
        if (result != None):
            if (dest != None) and returnToContainer:
                try:
                    len(result)
                    dest.extend(result)
                except TypeError:
                    dest.append(result)
            else:
                return result
# end evaluate


'''
Returns the appropriate flavor deque based on a given string 
'''
def getFlavor(flavorStr:str):
    if flavorStr == "CHOCOLATE":
        return _chocolate
    elif flavorStr == "VANILLA":
        return _vanilla
    else:
        raise ValueError(f"Invalid flavor deque \"{flavorStr}\"")
# end getFlavor

'''
Performs arithmetic (SWIRL) operation on the given deques.
Operation performed in the order <flavor1> <op> <flavor2>
'''
def swirl(flavor1:deque, flavor2:deque, op:str):
    val1, type1 = getLiteral(flavor1.pop())
    val2, type2 = getLiteral(flavor2.pop())

    if type1 == str or type2 == str:
        val1 = str(val1)
        val2 = str(val2)

    match op:
        case "+":
            return val1 + val2
        case "-":
            return val1 - val2
        case "*":
            return val1 * val2
        case "/":
            return val1 / val2
        case _:
            raise Exception(f"Invalid SWIRL operator \'{op}\'")
    # end match op
# end swirl
        
'''
Gets a literal (int, float, or str) from the input string. 
'''
def getLiteral(ipt:str):
    try:
        result = int(ipt)
        resultType = int
    except ValueError:
        try:
            result = float(ipt)
            resultType = float
        except ValueError:
            result = ipt
            resultType = str
    return result, resultType
# end getLiteral

'''
START INTERPRETER
'''
# Check for input args 
# If args give, parse the given file 
# Else, launch in REPL mode 
if len(sys.argv) > 1:
    # Start in file-parse mode 
    # Try to open given file name 
    try:
        fileName = sys.argv[1]
        file = open(fileName, "r")
        lines = file.readlines()
        file.close()
    except Exception as e:
        print(f"Error opening file: \n{e}")
        sys.exit(0)

    # Extract program from file
    try:
        extractProgram(lines)
    except Exception as e:
        print(f"Error parsing input file: \n{e}")
    
    # Parse file
    lineCount = 0
    while len(lines) > 0:
        try:
            parse(lines.pop(0))
            lineCount += 1
        except Exception as e:
            print(f"Error in line {lineCount}: \n{e}")
    # end while len(lines) > 0
else:
    # Start in REPL mode
    # Set up input
    line = ""
    
    # Start interpreter loop
    while line != "CLOCKOUT":
        # DEBUG Print flavor and cone status
        print(f"VANI: {_vanilla}")
        print(f"CHOC: {_chocolate}")
        print(f"CONE: {_cone}")

        # Get input
        line = input(">> ")

        # Parse input
        try:
            parse(expr=line, repl=True)
        except Exception as e:
            print(f"Error in \"{line}\": \n{e}")
    # end while line != "CLOCKOUT"
# end if len(sys.argv) > 1
