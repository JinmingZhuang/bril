import json
import sys


def myelimin():
    #delete instrs that assign to a vairble and this variable hasn't been used 
    prog = json.load(sys.stdin)
    for num,func in enumerate(prog['functions']):
        remove_ins = []
        instrs = func['instrs']
        length = len(instrs)
        for i in range(length):
            if 'dest' in instrs[i]:
                dest = instrs[i]['dest']
                flag = 0
                for j in range(i+1,length):
                    if 'args' in instrs[j]:
                        if dest in instrs[j]['args']:
                            flag = 1
                            break
                if flag == 0:
                    remove_ins.append(i)
        remove_ins.reverse()
        for i in remove_ins:
            del prog['functions'][num]['instrs'][i]
    
    with open("elimination.json", "w") as outfile:
        json.dump(prog, outfile)
        
            
            
if __name__ == '__main__':
    myelimin()