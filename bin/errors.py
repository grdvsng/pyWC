class CompatibilityError(Exception):

    def __init__(self, *args):
        msg = "\a\n\nSorry os: '{}' not supported.\nOnly NT or Posix.\n\n".format(*args)
        super().__init__(msg)

        
class InteriorClass(Exception):

    def __init__(self):
        msg = "\a\n\nCannot be created without WC.\n\n"
        super().__init__(msg)
        

class StartKeyError(Exception):
    
    def __init__(self, *args):
        msg = "\a\n\nStart key: '{}' not found, please try again.\n\n".format(*args)
        super().__init__(msg)
  
  
class InteriorSyntaxError(Exception):

    def __init__(self, msg):
        super().__init__('\n' + msg)
        
        
class InteriorExistsError(Exception):
    pass

ErrMsg = [
    "\a\nFile '{}' not exists! All values will read as str.",
    "Syntax error: '{}' can't be after '{}'",
]