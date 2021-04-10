import auto as a
import sys

def stringfyHiper(sv):
    comma = ";"
    return comma.join(sv)


def reachState(state, w):
    # print(state, w)
    for st in state:
        if(st[0] == w):
            return st[1]
            
def markStateFalse(table, marked):
    # print("enter: ", table, marked)
    if(table[marked] == None or table[marked] == False):
        table[marked] = False
        return
    else:
        # print("array: ", table[marked])
        for i in table[marked]:
            # print("i: ", i)
            if(i != marked):
                markStateFalse(table, i)

def afdToMinAfd(afd):
    
    #Tabela sem redundancia e trivalente
    tableValidator = {}
    for stTL in afd.state[1:]:
        for stTC in afd.state[:-1]:
            val = None
            if(stTC != stTL):
                
                #validar final com nao final
                # print(stTC, stTL, afd.final, stTC not in afd.final, stTL not in afd.final)
                if(not((stTC in afd.final and stTL in afd.final) or (stTC not in afd.final and stTL not in afd.final))):
                    val = False
                
                if(stTL > stTC):
                    tableValidator.update({(stTL, stTC): val})
                else:
                    tableValidator.update({(stTC, stTL): val})
    
    # print("t-0", tableValidator)
    
    # tableValidator = {
    #     ('q4', 'q0'): None, 
    #     ('q5', 'q0'): None, 
    #     ('q2', 'q1'): None, 
    #     ('q3', 'q1'): None, 
    #     ('q3', 'q2'): None, 
    #     ('q5', 'q4'): None, 
    #     ('q4', 'q1'): False, 
    #     ('q4', 'q2'): False, 
    #     ('q4', 'q3'): False, 
    #     ('q5', 'q1'): False, 
    #     ('q5', 'q2'): False, 
    #     ('q5', 'q3'): False, 
    #     ('q1', 'q0'): False, 
    #     ('q2', 'q0'): False, 
    #     ('q3', 'q0'): False
    # }
    #Check None states if Invalid
    for i in tableValidator:
        # print("\n --ON:", i, tableValidator[i])
        if(not(tableValidator[i] == False)):
            for word in afd.sigma:
                # print("\n\ntry", i[0], i[1], "in", word)
                stateA = reachState(afd.delta[i[0]], word)
                stateB = reachState(afd.delta[i[1]], word)
                # print("VALUE", stateA, stateB)
                if(stateA != stateB):
                    pres = 0
                    if(stateA > stateB):
                        pres = (stateA, stateB)
                    else:
                        pres = (stateB, stateA)

                    # print("CHECK", pres, "=", tableValidator[pres])
                    if(tableValidator[pres] == False):
                        # print("UPDATE TO FALSE",(i[0], i[1]),"of:   ", pres)
                        #era pra ser recursivo, mas Ele nao quer
                        # tempVis = [tableValidator[(i[0], i[1])]]
                        # for vis in tempVis:
                        #     if(vis != False):
                        #         print("-------UP-FALSE", tableValidator[vis], tempVis)
                        #         tempVis = tempVis + tableValidator[vis]
                        #         tableValidator[vis] = False 
                                
                        markStateFalse(tableValidator, (i[0], i[1]))
                        tableValidator[(i[0], i[1])] = False
                        break
                    else:
                        if(tableValidator[pres] == None):
                            # print("ADD-LINKED", i[0], i[1], "on", pres)
                            tableValidator[pres] = [(i[0], i[1])]
                        else:
                            # print("ADD-LINKED", i[0], i[1], "on", pres)
                            tableValidator[pres].append((i[0], i[1]))
                            tableValidator[pres] = list(set(tableValidator[pres]))
            # print("--ON:", tableValidator, "\n")

    
    #trnasitions
    newTrans = []
    for tv in tableValidator:
        if(tableValidator[tv] != False):
            # print("TABELA", tv, tableValidator[tv])
            if(len(newTrans) > 0):
                for ran in range(len(newTrans)):
                    if(tv[0] in newTrans[ran]):
                        newTrans[ran].append(tv[1])
                        newTrans[ran] = list(set(newTrans[ran]))
                    elif(tv[1] in newTrans[ran]):
                        newTrans[ran].append(tv[0])
                        newTrans[ran] = list(set(newTrans[ran]))
                    else:
                        newTrans.append([tv[1], tv[0]])
                
            else:
                newTrans.append([tv[1], tv[0]])
    
    # print(newTrans)
    # print("t-1", tableValidator)     
                 
    newDelta = {}
    newStatesAll = []
    newFinal = []
    newInit = ""
    for lop in afd.state:
        # print("\n\nINIT-", lop)
        w = lop
        for ntl in newTrans:
            if (w in ntl):
                w = stringfyHiper(ntl)
                break
        
        newFunc = []
        for wrd in afd.sigma:
            # print("\nWRD",wrd)
            for sat in afd.delta[lop]:
                if(sat[0] == wrd):
                    # print("afd", sat, wrd)
                    newTransit = sat[1]
                    # print("now", newTransit)
                    # newAppend = lop
                    for ntlw in newTrans:
                        if(sat[1] in ntlw):
                            # print("aqui", sat[0], stringfyHiper(ntlw))
                            newTransit = stringfyHiper(ntlw)
                            break
                    newFunc.append((wrd, newTransit))
                    
                    # print(lop, afd.final, afd.init, newTransit)
                    if(lop in afd.final):
                        newFinal.append(w)
                    
                    if(lop == afd.init):
                        newInit = w
                    
        # print("------NEW", newFunc)
        newDelta.update({w: newFunc})
    #new states
    for nsin in newDelta:
        # print(nsin, newDelta[nsin])
        newStatesAll.append(nsin)
        for childres in newDelta[nsin]:
            newStatesAll.append(childres[1])
        newStatesAll = list(set(newStatesAll))
    # print(newFinal)
    newFinal = list(set(newFinal))
    # print("END:", newStatesAll, newDelta, newFinal)
    
    minAfd = a.auto(afd.sigma, newStatesAll, newDelta, newInit, newFinal)
    return minAfd

def concatState(st, delta, w):
    print("CONCAT", st, delta)
    return

def stringfy(sv):
    comma = ","
    return comma.join(sv)

def afnToAfd(afn):
    
    newDelta = {}
    newFinal = []
    
    #NEW STATES
    visitor = [afn.init]
    for i in visitor:
        # print("\n\ni:", i, visitor)
        split = i.split(",")
        newStF = []
        # isFinal = False
        for w in afn.sigma:
            # print("W:", w)
            newWord = []
            for s in split:
                # print("S:", s)
                if(s in afn.delta):
                    for tupla in afn.delta[s]:
                        if(tupla[0] == w):
                            # print(w, "--->",tupla[1], afn.final, s)
                            if(tupla[1] not in newWord): 
                                newWord.append(tupla[1])
                                
                            if(s in afn.final or tupla[1] in afn.final):
                                newFinal.append(s)
                                newFinal.append(tupla[1])
                                # isFinal = True
                            
            # print("END:", i, w, newWord)
            if(newWord != []):
 
                newQ = stringfy(newWord)
                
                # if(s not in newFinal and isFinal):
                #     newFinal.append(s)
                
                # print("CHECK", newQ, "==", visitor, "Q:", newQ not in visitor)
                # print("NEW:", i,": (", w, newQ, ")")
                newStF.append((w, newQ))
                if(newQ not in visitor):
                    # print("VIS:", newQ)
                    visitor.append(newQ)
                    
        if(newStF != []):            
            newDelta.update({
                i: newStF
            })
    
    # print(newDelta)
    #parcial -> completa
    
    silkUsed = False
    for vi in visitor:
        # print("\n\nV:", vi)
        if(vi in newDelta):
            dontHave = list(set(afn.sigma))
            for si in newDelta[vi]:
                #(a,b)
                # print(si)
                for wi in afn.sigma:
                    # print(wi)
                    if(si[0] == wi):
                        # print("REMOVE", wi)
                        dontHave.remove(wi)
                
            # print("ADD", vi, dontHave)
            for nw in dontHave:
                silkUsed = True
                newDelta[vi].append((nw, "q$"))
        else:
            dontHave = []
            for win in afn.sigma:
                # print("ADD", vi, win)
                silkUsed = True
                dontHave.append((win, "q$"))
            newDelta.update({
                vi: dontHave
            })

    if(silkUsed):
        silkStates = []
        for silkS in afn.sigma:
            silkStates.append((silkS, "q$"))
        newDelta.update({
            "q$": silkStates
        })
        visitor.append("q$")

    newFinal = list(set(newFinal))
    newFinalSelect = []
    for nf in newFinal:
        if(nf in afn.final):
            for ast in visitor:
                # print(ast, nf)
                splitW = ast.split(",")
                if(nf in splitW and ast in visitor):
                    newFinalSelect.append(ast)
                    break
    
    newFinalSelect = list(set(newFinalSelect))
    # print("final", newFinal)
    afd = a.auto(afn.sigma,visitor,newDelta,afn.init,newFinalSelect)
    return afd

def feAuto(delta, state):
    # print("fe:", delta, state)
    aux = [state]
    if(state in delta):
        g = delta[state]
        # print(g)
        for i in g:
            if(i[0] == "$"):
                # print(i[1])
                aux = aux + feAuto(delta, i[1])
    return aux

def afneToAfn(afne:a):
    # afne.printAuto()
    closure = {}
    for i in afne.state:
        fe = feAuto(afne.delta, i)
        aux = {
            i: fe
        }
        closure.update(aux)
    
    # print("f", closure)
    
    table = {}
    
    for w in afne.state:
        table.update({w: []})
        
    for k in afne.state:
        for h in afne.sigma:
            if(h != '$'):
                for j in closure[k]:
                    if(j in afne.delta):
                        for l in afne.delta[j]:
                            # print(k, j, h, l, "CASE1")
                            if(l[0] == h):
                                # print("add", k, h, "->", closure[l[1]])
                                aux = (h, closure[l[1]])
                                table[k].append(aux)
                    
    # print(table)
                
    newDelta = {}
    newState = [afne.init]
    newSigma = []
    pState = []
    
    for cand in afne.state:
        if(table[cand] != []):
            pState.append(cand)
            
            
    while(len(pState) > 0):
        # print(pState)
        nState = pState.pop()
        if(nState in newDelta):
            pass
        else:
            obj = []
            # print(table)
            for u in table[nState]:
                # print(u)
                for ve in u[1]:
                    # print(u[0], ve)
                    pState.append(ve)
                    if(ve not in newState): newState.append(ve)
                    if(u[0] not in newSigma): newSigma.append(u[0])
                    obj.append((u[0], ve))
                aux = {
                    nState: obj
                }
                newDelta.update(aux)
    
    newFinal = []
    
    for fin in newState:
        for endAuto in afne.final:
            if(endAuto in closure[fin]):
                newFinal.append(fin)
    
    # print(newFinal)
    
    #excluindo estados na alcancaveis:
    parseDelta = {}
    for nse in newState:
        if nse in newDelta:
            parseDelta.update({
                nse: newDelta[nse]
            })
    
    afn = a.auto(newSigma,newState,parseDelta,afne.init,newFinal)
    
    return afn

def match(er, w):
    if(afdToMinAfd(afnToAfd(afneToAfn(erToAfne(er)))).accepted(w)):
        return "OK"
    return "Not OK"

def delSpace(string:str):
    string.replace(" ","")
    string.replace("'", "")
    return string

def buildAutoEmpty(w:str, d:int):
    print("BUILD-EM", w, d)
    # sigma = 
    # final = 1
    # init = 2
    # state = 3
    # delta = 4
    # return a.auto(sigma, state, delta, init, final)
    return 0

def buildAutoEps(w:str, d:int):
    print("BUILD-EPS", w, d)
    # sigma = 
    # final = 1
    # init = 2
    # state = 3
    # delta = 4
    # return a.auto(sigma, state, delta, init, final)
    return 0

def buildAutoVar(w:str, d:int):
    # print("BUILD-VAR", w, d)
    sigma = [w]
    final = ['qf'+str(d)]
    init = 'q0'+str(d)
    state = [init, final[0]]
    delta = {init : [(w, final[0])]}
    auto = a.auto(sigma, state, delta, init, final)
    # auto.printAuto()
    return auto
    

def afnePlus(a1, a2, d):
    # print("AFNE-PLUS")
    sigma = ["$"] + a1.sigma + a2.sigma
    sigma = list(set(sigma))
    final = ['qf'+str(d)]
    init = 'q0'+str(d)
    state = [init, final[0]] + a1.state + a2.state
    state = list(set(state))
    delta = {
        init : [("$", a1.init), ("$", a2.init)], 
        a1.final[0]: [("$", final[0])], 
        a2.final[0]: [("$", final[0])]
    }
    delta.update(a1.delta)
    delta.update(a2.delta)
    auto = a.auto(sigma, state, delta, init, final)
    # auto.printAuto()
    return auto

def afneStar(a1, d):
    # print("AFNE-START")
    sigma = ["$"] + a1.sigma
    sigma = list(set(sigma))
    final = ['qf'+str(d)]
    init = 'q0'+str(d)
    state = [init, final[0]] + a1.state
    state = list(set(state))
    delta = {}
    delta.update(a1.delta)
    new = {
        init: [("$", a1.init), ("$", final[0])],
        a1.final[0]: [("$", a1.init), ("$", final[0])]
    }
    delta.update(new)
    auto = a.auto(sigma, state, delta, init, final)
    # auto.printAuto()
    return auto

def afneDot(a1, a2, d):
    # print("AFNE-DOT")
    sigma = ["$"] + a1.sigma + a2.sigma
    sigma = list(set(sigma))
    final = a2.final
    init = a1.init
    state = [init, final[0]] + a1.state + a2.state
    state = list(set(state))
    delta = {
        a1.final[0]: [("$", a2.init)]
    }
    delta.update(a1.delta)
    delta.update(a2.delta)
    auto = a.auto(sigma, state, delta, init, final)
    # auto.printAuto()
    return auto

def stripFunAuto(string:str):
    idx = 1
    pos = 0
    for i in string:
        if(i == '+' or i == '.'):
            idx += 1
        
        if(i == "*" and idx == 0):
            return [string[pos+1:-2], []]
            
        if(i == ','):
            idx -= 1
            if(idx == 0):
                return [string[0:pos], string[pos+1:]]
                
        pos += 1
        
    return [string, []]

def getSymAuto(w:str):
    a = {}
    a['value'] = w[0]
    aux = stripFunAuto(w[2:-1])
    a['left'] = aux[0]
    a['right'] = aux[1]
    return a
    
def auxErtoAfne(w:str, d:int):
    if(len(w) == 0):
        return buildAutoEmpty(w, d)
    if(w == '$'):
        return buildAutoEps(w, d)
    if(len(w) == 1):
        return buildAutoVar(w, d)
    
    nAuto = getSymAuto(w)
    d = d*2
    # print("nAuto", nAuto, d)
    if(nAuto['value'] == '+'):
        return afnePlus(auxErtoAfne(nAuto['left'], d+1), auxErtoAfne(nAuto['right'], d+2), d) 
    if(nAuto['value'] == '.'):
        return afneDot(auxErtoAfne(nAuto['left'], d+1), auxErtoAfne(nAuto['right'], d+2), d) 
    if(nAuto['value'] == '*'):
        return afneStar(auxErtoAfne(nAuto['left'], d+1), d)

def erToAfne(w:str):
    return auxErtoAfne(w, 0)

#DESENVOLVIMENTO:
# mock = "+(.(a,b),a)"
# mock = "+(a,b)"
mock = ".(a,a)"
# mock = "*(a)"
# mock = "+(.(*(a),b),c)"
# mock = "*(+(a,.(b,c)))"
# mock = ".(*(a),+(.(a,a),.(b,b)))"
# mock = '+(.(+(a,b),c),d)'
#( ( 11 * 0 + 0 ) ( 0 + 1 )* 0* 1* ) 
# mock = ".(+(+(*(.(1,1)),0),0),*(+(0,1)))"

# tip = erToAfne(mock, 0)
# tip.printAuto()
# tip1 = afneToAfn(tip)
# tip1.printAuto()

# test = {
#     'q0': [('a', 'q0'),('a', 'q1')], 
#     'q1': [('b', 'q2'),('b', 'q3'),('b', 'q5')], 
#     'q2': [('a', 'q1')], 
#     'q3': [('c', 'q4')],
#     'q4': [('c', 'q4')], 
#     'q5': [('c', 'q6')],
#     'q6': [('d', 'q6')]
# }
# tip2 = afnToAfd(a.auto(['a', 'b', 'c', 'd'], ['q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6'], test, 'q0', ['q4', 'q5', 'q6']))
# tip2 = afnToAfd(tip1)
# tip2.printAuto()

# test = {
#     'q0': [('a', 'q2'),('b', 'q1')], 
#     'q1': [('a', 'q1'),('b', 'q0')],
#     'q2': [('a', 'q4'),('b', 'q5')], 
#     'q3': [('a', 'q5'),('b', 'q4')], 
#     'q4': [('a', 'q3'),('b', 'q2')], 
#     'q5': [('a', 'q2'),('b', 'q3')]
# }

# test = {
#     'q0': [('a', 'q2'),('b', 'q1')], 
#     'q1': [('a', 'q1'),('b', 'q0')],
#     'q2': [('a', 'q4'),('b', 'q5')], 
#     'q3': [('a', 'q5'),('b', 'q4')], 
#     'q4': [('a', 'q3'),('b', 'q2')], 
#     'q5': [('a', 'q2'),('b', 'q3')]
# }

# test = {
#     'q0': [('a', 'q3'),('b', 'q1')], 
#     'q1': [('a', 'q2'),('b', 'q5')],
#     'q2': [('a', 'q2'),('b', 'q5')], 
#     'q3': [('a', 'q0'),('b', 'q4')], 
#     'q4': [('a', 'q2'),('b', 'q5')], 
#     'q5': [('a', 'q5'),('b', 'q5')] 
# }

# tip3 = afdToMinAfd(tip2)
# tip3 = afdToMinAfd(a.auto(['a', 'b'], ['q5', 'q4', 'q1', 'q2', 'q3', 'q0'], test, 'q0', ['q4', 'q1', 'q2']))
# tip3.printAuto()

# if(match(".(a,a)", "a")):
#     print("OK")
# else:
#     print("Not OK")


# print(sys.argv)

if (__name__ == '__main__'):
    if sys.argv[1] == "-f":
        arquivo = sys.argv[2]
        palavra = sys.argv[3]
        
        file1 = open(arquivo, 'r')
        Lines = file1.readlines()
        for line in Lines:
            # print(line.strip())
            # line = str(line)
            retorno = match(line.strip(), palavra)

            print("match("+line.strip()+","+" '"+palavra+"' "+") == "+retorno)
    else:
        er = sys.argv[1]
        palavra = sys.argv[2]
        retorno = match(er, palavra)

        print("match("+er+","+" '"+palavra+"' "+") == "+retorno)

# print(tip3.accepted("ab"))