import definitions


def Interpret(line:str):
    '''Splits a nest/nests into their pairs and evaluates them backwards'''
    num_nest_opens = line.count("(")
    num_nest_closes = line.count(")")

    if num_nest_closes == num_nest_opens and num_nest_closes != 0 :
        # function-test-(function-test2-(function-test3-3))
        nests = line.split("(")
        
        nests[len(nests)-1] = nests[len(nests)-1].removesuffix(")"*num_nest_closes)

        nests.reverse()
            
        prev_output = ""
        for nest in nests :
            prev_output = Solve_Nest(nest+str(prev_output))
        
        return prev_output
    else :
        result = Solve_Nest(line)
        return result


def load(path : str):
    try: 
         f = open(path , 'r')
    except FileNotFoundError :
         raise Exception("Invalid path")
    
    doc = f.readlines()
    f.close()

    i = 0
    for line in doc :
        pos = line.find("<!--{")
        if pos > -1 :
            chunk = line[pos+len("<!--{"):line.index("}")]
            
            doc[i] = line[:pos] + TypeCast(Interpret(chunk)) + line[line.index("}")+len("}-->"):]

        i = i + 1

    return bytes("".join(doc) , 'UTF-8')

def load_component(path , registration_id): 
    try: 
         f = open(path , 'r')
    except FileNotFoundError :
         raise Exception("Invalid path")
    
    doc = f.readlines()
    f.close()

    i = 0
    for line in doc :
        pos = line.find("<!--{")
        if pos > -1 :
            chunk = line[pos+len("<!--{"):line.index("}")]
            
            doc[i] = line[:pos] + TypeCast(Interpret(chunk)) + line[line.index("}")+len("}-->"):]

        i = i + 1

    doc.insert(0 , "<!--{~"+registration_id+"~}-->")
    return bytes("".join(doc) , 'UTF-8')   
            
def Solve_Nest(nest:str):
    if nest == '':
        return ''
    nest = nest.split("-")
    
    if nest[0] == 'variable':
        return str(definitions.namespace["variable"][nest[1]])

    elif nest[0] == 'function':
        return definitions.namespace["function"][nest[1]](nest[2].split(","))
    
    else :
        return " There seems to be an issue. Check your nesting "

def TypeCast(input):
    if type(input) != type(str):
        return input.__str__()
    else : 
        return input