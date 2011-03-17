
class AbstractCollection():
    def __init__(self, variant, *args):
        self.variant = variant
        self.items = list(args)

    def append(self, section):
        self.items.append(section)

    def remove(self, section):
        self.items.remove(section)

    def __getitem__(self, item):
        return self.items[item]

    def __setitem__(self, item):
        return self.items[item]
    
    def __repr__(self):
        return '{0}({1})'.format(self.variant, str(self.items))

    def __str__(self):
        return self.__repr__()

class Program(AbstractCollection):
    def __init__(self, *args):
        AbstractCollection.__init__(self, 'Program', *args)

    def __str__(self):
        return '\n'.join([str(i) for i in self.items])

class Section(AbstractCollection):
    def __init__(self, name, *args):
        AbstractCollection.__init__(self, 'Section', *args)
        self.name = name

    def __str__(self):
        res = '{0}:\n'.format(self.name)
        res += '\n'.join(['\t'+str(i) for i in self.items])
        
        return res

class Command(AbstractCollection):
    def __init__(self, name, *args):
        AbstractCollection.__init__(self, 'Command', *args)
        self.name = name

    def __str__(self):
        return '{0} {1}'.format(self.name, ' '.join([str(i) for i in self.items]))

class Imports(AbstractCollection):
    def __init__(self, *args):
        AbstractCollection.__init__(self, 'Imports', *args)

    def __str__(self):
        return ', '.join(['{0[0]}::{0[1]}'.format(i) for i in self.items]) 

class Register():                                                               
    def __init__(self, number):                                                 
        self.number = number
    
    def __str__(self):                                                          
        return 'r%s' % self.number
    
    def __repr__(self):                                                         
        return self.__str__() 

class FunctionCall():
    def __init__(self, name, *args):
        self.name = name
        self.args = args

    def __str__(self):
        return '{0}({1})'.format(self.name, ' '.join([str(i) for i in self.args]))

    def __repr__(self):
        return 'FunctionCall({0.name}, {0.args})'.format(self)
