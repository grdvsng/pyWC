from sys        import argv, getsizeof, path as syspath   # For read start args.    
from os.path    import exists, abspath,dirname            # For work with files.      
from os         import (
    system as cmd, 
    name  as os_name,
    chdir as workdir
)   # For interface only.

syspath.append(abspath(dirname(__file__)))
syspath.append('..\\')
from bin.errors import *    

class InteriorSet: 
    # Special diction with prompt command for user OS.
    _os    = {
        'nt': {
            'pause': 'pause',
            'cls':   'cls',
            'sleep': 'timeout /t 3 >nul',
            'color': 'color f9'
            
        },
        'posix': {
            'pause': None,
            'cls':   'clear',
            'sleep': 'sleep 3',
            'color': ' '
        }
    }
    
    _values       = ['l,w,c,h,help,-q', '--l,--w,--c,--h,--h,q']  
    _is_interface = False
    _inp_msg      = """\n\n------{}(file)------\nPlease, enter file(s) full path (separation ' ').> """

    _inp          = lambda s, x: input(s._inp_msg.format(x[5:len(x)])).split(" ")
    _interface    = '''
\tpyWC utility version 0.9
{0}
\t'--l' Lines count.
\t'--w' Word  count.
\t'--c' Bytes count.
\t'--h' Help.
\n{0}
author: grdvsng@gmail.com
{0}
    '''.format('--'*20)
    
    _errors_dict = [
        CompatibilityError,
        InteriorClass,
        StartKeyError,
        InteriorSyntaxError,
        InteriorExistsError
    ] 

    def __init__(self, name):
        # Check os because will use modul os.system.
        if name in self._os: self._os = self._os[name] 
        else:                self._errors(0, [name]) 
        
    def _errors(self, key, txt=[]):
        _type = self._errors_dict[key]
        raise _type(*txt) if txt else _type()
    
    def __call__(self, key, txt=None):
        if isinstance(key, str): key = [key] 
        
        for i in key:
            command = self._os[i] 
            
            if txt: print(txt)
            if command: cmd(command)
            else:       input('Please press Enter.> ')
            
    def _exists(self, file):
        if exists(r'%s' % file): return True
        else:
            msg = "\a\nFile '{}' not exists, will read as str.".format(file)
            self("pause", msg)
            return False       

    def _val_parse(self, val):
        ''' Method _val_parse class InteriorSet.
            Arguments:
                val - str from menu input or start argv.
                
            Description:
                check value must be from self._values[0] if mistake try change to correct.
                
        '''
        
        value     = val.lower().strip()
        _cur_list = self._values[1].split(",")
        _err_list = self._values[0].split(",")
        
        if value in _err_list: 
            value = _cur_list[_err_list.index(value)]
        elif len(value) == 2 and value[1:2] in _err_list: 
            value = _cur_list[_err_list.index(value[1:2])]
        
        if value not in _cur_list: return False    
        else:                      return value
    
    def _file_parse(self, file): 
        ''' Method _file_parse class InteriorSet.
            Arguments:
                file - str with value from class file read methods. 
                
            Description:
                count values.
                
        '''
        
        lines = 0
        
        for line in file: 
            lines += 1
        
        if lines > 0: return lines 
        else:         return None 
               
    def _parse(self, args):
        ''' Method _parse class WC.
            
            Arguments:
                args - tuple with args or str.
                
            Description:
               parse args and return methods or error.
            
        '''

        files     = []   # list with file path or special str.
        curmeth   = None # WC Main method.
        # If not main can call with args list if not need use separator ' '.
        parametrs = args.split(" ") if isinstance(args, str) else args 
        
        if len(args) == 0: 
            if not self.debug: return self.menu
            else: return
        
        for i in parametrs:
            if self._val_parse(i):
                val = self._val_parse(i)
                
                if not curmeth: curmeth = 'self.%s' % self._args[val] if val != 'q' else quit()
                else: 
                    if val == '--h':
                        files   = curmeth
                        curmeth = 'self._help'
                        break  
                        
                    else: 
                        msg = "Syntax error: '{}' can't be after '{}'".format(val, curmeth) 
                        if self._is_interface: self('sleep', msg) ; curmeth = None
                        else: self._errors(3, [msg])
                          
            else: files.append(i)
            
        if curmeth: 
            if not files and '_help' not in str(curmeth): 
                while 1 > 0:
                    files = self._inp(curmeth)
                    
                    if 'q' == files[0]:   quit()
                    if len(files[0]) > 0: break
                    else: 
                        self('cls')
                        print('Please pass value or press q for exit.')
                    
            files = 'self' if 'help' in str(curmeth) and 'self.' not in str(files) else files
            
            self('sleep', '%s' % str(curmeth)[5:len(curmeth)])
            command = "{}({})".format(curmeth, files)
            eval(command)
                         
        else: 
            msg = "Keys: '{}', not found.".format(files)
            if self._is_interface: self('pause', msg)  
            else: self._errors(2, [files])
        
    def _result(self, D):
        result = {}
        bad_msg = msg = ''
        
        for k,v in D.items():
            if D[k]: 
                result[k]  = v
                msg       += '\nfile: %s: %s' % (k, v)
            else: bad_msg += '\nfile: %s, lines not found.' % k
            
        if len(msg) > 0: 
            self('pause', msg + bad_msg)
            return result
        else:
            if len(bad_msg) > 0: self('pause', bad_msg) 
            return
            

class WC(InteriorSet):
    ''' Class WC.
        Main class of script.
        WC analog of WC Linux utility.
        
        Public methods:
            
            lines_count(file) - return dict format {file: lines} - start key: '--l'
            words_count(file)  - return dict format {file: words} - start key: '--w'
            bytes_count(file) - return dict format {file: bytes} - start key: '--c'
                *all method return in int format or list of int.
        
        Special method:
            _help - return doc of method which called. - start key: '--h' or 'help'

        can start scripts without key:
            examples:
                py pyWC .\my.txt --l
                py pyWC .\my.txt your.txt --l 
                
    '''
    
    # True launch arguments.
    _args = {
        '--l': 'lines_count',
        '--w': 'words_count',
        '--c': 'bytes_count',
        '--h': '_help ',
        'q':   quit
    } 
    
    def __init__(self, os, _is_interface=False, debug=False):
        self.debug = debug  # special for test.
        self._is_interface = _is_interface
        
        super().__init__(os)
        self._parse(argv[1:len(argv)])
              
    def lines_count(self, files):
        ''' Method lines_count class WC.
            Arguments:
                files - file or list of files for parse.
                
            Description:
                reading file and count lines and return value.
            
            examples:
                $home> '\my.txt' --l;
                $home> 12
            
            *return values {k: v}, where:
                k - is file path; 
                v - lines count.
                
        '''
        
        lines = {}
        
        for f in files:
            f = abspath(f)
            if self._exists(f): 
                with open(f, 'r') as file: 
                    lines[f] = self._file_parse(file.readlines())
                    
            else: 
                _lines = (str(files).rfind('\n')) 
                lines['stdin'] = _lines if _lines > 0 else None
                break
                
        if len(lines) > 0: return self._result(lines)
        else: return False
        
    def words_count(self, files):
        ''' Method words_count class WC.
            Arguments:
                files - file or list of files for parse.
                
            Description:
                reading file and count word and return value.
            
            examples:
                $home> '\my.txt' --c;
                $home> 4
                
            *return values {k: v}, where:
                k - is file path; 
                v - word count.
            
        '''
        words = {}
        
        for f in set(files):
            f = abspath(f)
            if self._exists(f): 
                with open(f, 'r') as file: 
                    _words   = file.read().replace("\n", " ").split(" ")
                    words[f] = self._file_parse(_words)
            else: words['stdin'] = len(files); break
                
        result = self._result(words)
        return result
        
    def bytes_count(self, files):
        ''' Method bytes_count class WC.
            Arguments:
                file - file or list of files for parse.
                
            Description:
                reading file and count bytes and return value.
            
            examples:
                $home> '\my.txt' --w;
                $home> 10
            
            *return values {k: v}, where:
                k - is file path; 
                v - bytes count.
              
        '''
        
        _bytes = {}
        
        for f in set(files):
            f = abspath(f)
            if self._exists(f): 
                with open(f, 'rb') as file: 
                    _bytes[f] = self._file_parse(file.read())
            else: _bytes['stdin'] = getsizeof(files); break
            
        result = self._result(_bytes)
        return result
        
    @property
    def menu(self):
        self(['cls', 'color'])
        
        while 0 < 1:
            print(self._interface)
            response = self._parse(input('Please, choice any value or press q(exit)> '))
            self('cls')
            
    def _help(self, method):
        if self.debug: return
        self('cls')
        # Only when you press --h with --h
        method = self if '_help' in str(method) else method
        self('pause',  method.__doc__)
  

if __name__ == '__main__':
    script = WC(os_name, _is_interface=True)
   