from sys import argv, path as syspath

syspath.append(r'..\\')
from bin.wc import *

def test(n):
    #CompatibilityError
    def test1():
        try: script = WC('ns')
        except CompatibilityError: pass
    
    #Clean
    def test2(): 
        script = WC('nt', debug=True)
    
    # StartKeyError
    def test3(): 
        argv.append('1')
        argv.append('2')
        try: script = WC('nt')
        except StartKeyError: 
            argv.remove('1')
            argv.remove('2')
    
    # InteriorSyntaxError
    def test4(): 
        argv.append('l')
        argv.append('w')
        try: script = WC('nt')  
        except InteriorSyntaxError:
            argv.remove('l')
            argv.remove('w')
    
    # Help
    def test5(): 
        argv.append('l')
        argv.append('h')
        script = WC('nt', debug=True)
        argv.remove('l')
        argv.remove('h')
    
    
    def test6(): 
        out = r'test.txt'
        file = open(out,'a')
        for i in range(0, 9):
            file.write('%s' % i)
        file.close()
        script = WC('nt', debug=True)
        
        script.lines_count(out)
        script.words_count(out)
        script.bytes_count(out)
        
    exec("test{}(); print('''---Done!---\n''')".format(n))
    
if __name__ == '__main__':
    for i in range(1, 7):
        print('---step {}---\n'.format(i))   
        test(i)