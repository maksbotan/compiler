
import sys
from ply import lex, yacc
from util import Program, Section, Register, Imports, Command, FunctionCall

class Parser():

    def  __init__(self):
        self.lexer = lex.lex(module=self)
        self.parser = yacc.yacc(module=self)

        self.sections = {}

    tokens = (
        'HEX',
        'NUMBER',
        'FLOAT',
        'LPAR',
        'RPAR',
        'WORD',
        'STRING',
        'POINTER',
        'REG',
    #    'QUOT',
        'COLON',
        'INDENT',
        'SPACE',
        'COMMA',
        'NEWLINE',
    )

    t_LPAR = r'\('
    t_RPAR = r'\)'
    t_POINTER = r'&'

    @lex.Token(r'r\d')
    def t_REG(self, t):
        t.value = Register(int(t.value[1]))
        return t
    
    t_STRING = r'"[\w\.\?' + "'" + '\s,\\\\n]+"'
    t_WORD = r'[\w\.\?]+'
#    t_QUOT = '"'
    t_COLON = ':'
    t_INDENT = r'\t+'
    t_COMMA = ','
    t_NEWLINE = r'\n'

    t_ignore = ''

    @lex.Token(r'0x[abcdef\d]+')
    def t_HEX(self, t):
        t.value = int(t.value[2:], 16)
        return t

    @lex.Token(r'\d+\.\d+')
    def t_FLOAT(self, t):
        t.value = float(t.value)
        return t

    @lex.Token(r'\d+')
    def t_NUMBER(self, t):
        t.value = int(t.value)
        return t

    @lex.Token(r'[ ]+')
    def t_SPACE(self, t):
        t.value = ' '
        return t

    def t_error(self, t):
        raise TypeError('Error on %s' % t.value)

    def lex(self, text):
        self.lexer.input(text)
        return iter(self.lexer.token, None)

    def p_program_single(self, p):
        'program : section'
        self.program = Program(p[1])
        print 'p_program: %s' % list(p)

    def p_program(self, p):
        'program : program section'
        self.program.append(p[2])

    def p_section(self, p):
        'section : section_name section_block'
        p[0] = Section(p[1], *p[2])
        print 'p_section: %s' % list(p)

    def p_section_name(self, p):
        'section_name :  WORD COLON NEWLINE'
        print 'section_name: %s' % list(p)
        p[0] = p[1]

    def p_section_block_single(self, p):
        'section_block : section_line'
        p[0] = [p[1]]

        print 'section_block_single: %s' % list(p)

    def p_section_block(self, p):
       'section_block : section_block section_line'
       if isinstance(p[1], list):
           p[1].append(p[2])
           p[0] = p[1]
       else:
           p[0] = [p[1], p[2]]

       print 'section_block: %s' % list(p)

    def p_section_line(self, p):
        'section_line : INDENT statement NEWLINE'
        p[0] = p[2]
        print 'section_line: %s' % list(p)

    def p_statement(self, p):
        'statement : WORD SPACE args'
        p[0] = Command(p[1], *p[3])

        print 'p_statement: %s' % list(p)

    def p_statement_import(self, p):
        'statement : comma_list'
        p[0] = Imports(*p[1])
        print 'p_statement: %s' % list(p)

    def p_arg(self, p):
        """
        arg : NUMBER
        arg : HEX
        arg : STRING
        arg : WORD
        arg : call
        arg : string
        arg : REG
        arg : import
        """
        p[0] = [p[1]]
        print 'p_arg: %s' % list(p)

    def p_args_single(self, p):
        'args : arg'
        p[0] = p[1]

        print 'p_args: %s' % list(p)

    def p_args(self, p):
        'args : args SPACE arg'
        print 'DEBUG %s' % list(p)
        if isinstance(p[1], list):
            p[0] = p[1] + p[3]
        else:
            p[0] = [p[1]]+p[3]

        print 'p_args: %s' % list(p)

    def p_comma_list_s(self, p):
        'comma_list : arg'
        p[0] = p[1]

    def p_comma_list(self, p):
        'comma_list : comma_list COMMA SPACE arg'
        if isinstance(p[1], list):
            p[0] = p[1] + p[4]
        else:
            p[0] = [p[1]]+p[4]

        print 'p_comma_list: %s' % list(p)

    def p_import(self, p):
        'import : WORD COLON COLON WORD'
        p[0] = (p[1], p[4])
        print 'p_import: %s' % list(p)

#    def p_fill(self, p):
#        """
#        fill : WORD LPAR NUMBER RPAR
#        fill : WORD LPAR HEX RPAR
#        """

#        p[0] = {'type': 'fill', 'data': p[3]}

    def p_string(self, p):
        'string : STRING'
        p[0] = p[1]

        print 'p_string: %s' % list(p)

    def p_call(self, p):
        'call : WORD LPAR args RPAR'
        p[0] = FunctionCall(p[1], *p[3])

    def p_error(self, p):
        raise TypeError('Error on %s and %s, next: %s' % (p.value, p.type, yacc.token()))

    def parse(self, text):
        self.parser.parse(text)

if __name__ == '__main__':
    if not len(sys.argv) == 2:
        print 'Usage: %s FILENAME' % sys.argv[0]
        sys.exit(1)

    program = open(sys.argv[1]).read()

    p = Parser()
    p.parse(program)
    print (p.program)
