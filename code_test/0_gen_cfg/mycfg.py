import json
import sys
from collections import OrderedDict

TERMINATORS = ['jmp','br','ret']

def form_blocks(body):
    cur_block = []
    for instr in body:
        if 'op' in instr: # An actrual ins
            cur_block.append(instr)
            
            #check for terminators
            if instr['op'] in TERMINATORS:
                yield cur_block
                cur_block = []
        else: # A label
            if cur_block:
                yield cur_block
            cur_block = [instr]
            
    if cur_block:
        yield cur_block

def block_map(blocks):
    out = OrderedDict()
    for block in blocks:
        if 'label' in block[0]:
            name = block[0]['label']
            block = block[1:]
        else:
            name = 'b{}'.format(len(out))
        out[name] = block
        
    return out
    
def mycfg():#seperate the instrs to blocks
    prog = json.load(sys.stdin)
    for func in prog['functions']:
        for block in form_blocks(func['instrs']):
            print(block)

def mycfg1():#name the blocks with labels
    prog = json.load(sys.stdin)
    for func in prog['functions']:
        name2block = block_map(form_blocks(func['instrs']))
        print(name2block)  

def get_cfg(name2block):
    """
    Given the name-to-block map, produce the cfg based on the dependencies
    """   
    out = {}
    for i, (name, block) in enumerate(name2block.items()):
        last = block[-1]
        if last['op'] in ['jmp','br']:
            succ = last['labels']
        elif last['op'] == 'ret':
            succ = []
        else:
            if i == len(name2block)-1:
                succ=[]
            else:
                succ = [list(name2block.keys())[i+1]]
        
        out[name] = succ
    return out
     
def mycfg2():#generate the cfg
    prog = json.load(sys.stdin)
    for func in prog['functions']:
        name2block = block_map(form_blocks(func['instrs']))
        for name, block in name2block.items():
            print(name)
            print(' ',block)
        cfg = get_cfg(name2block)
        print(cfg)

def mycfg_visual():#generate the cfg with graph
    prog = json.load(sys.stdin)
    for func in prog['functions']:
        name2block = block_map(form_blocks(func['instrs']))
        cfg = get_cfg(name2block)
        print('digraph {} {{'.format(func['name']))
        for name in name2block:
            print(' {};'.format(name))
        for name, succs in cfg.items():
            for succ in succs:
                print(' {} -> {}'.format(name,succ))
        print('}')     

if __name__ == '__main__':
    mycfg_visual()