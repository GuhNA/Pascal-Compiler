#Importar o "lex" do PLY
from lex import lex

#tokens
tokens = ("INICIALIZADOR","QUALIFICADORVAR","QUALIFICADORCONST","ABRE_CHAVES","FECHA_CHAVES","REAL","SE","SENAO","ENTAO",
        "ATRIBUICAO","TIPO_DADO", "OPERADOR_ARITMETICO", "SEPARADOR_CMD", "CONSTANTE_INTEIRA", "OPERADOR_RELACIONAL", "ASPAS",
          "ABRE_PARENTESES","FECHA_PARENTESES", "OPERADOR_LOGICO", "SEPARADOR","FLOAT", "TIPADOR","REPETICAOFOR","REPETICAOWHILE",
          "LEITOR","PRINT","UPORDOWN","DO","IDENTIFICADOR")

'''Alfabeto case insensitive
(a|A)(b|B)(c|C)(d|D)(e|E)(f|F)(g|G)(h|H)(i|I)(j|J)(k|K)(l|L)(m|M)
(n|N)(o|O)(p|P)(q|Q)(r|R)(s|S)(t|T)(u|U)(v|V)(w|W)(x|X)(y|Y)(z|Z)
'''

#tipos de dados
integer = "((i|I)(n|N)(t|T)(e|E)(g|G)(e|E)(r|R))"
real = "((r|R)(e|E)(a|A)(l|L))"
boolean = "((b|B)(o|O)(o|O)(l|L)(e|E)(a|A)(n|N))"
char = "((c|C)(h|H)(a|A)(r|R))"
string = "((s|S)(t|T)(r|R)(i|I)(n|N)(g|G))"
#definindo cada Definição
t_QUALIFICADORVAR= "((v|V)(a|A)(r|R))"
t_QUALIFICADORCONST= "((c|C)(o|O)(n|N)(s|S)(t|T))"
t_ABRE_CHAVES = "((B|b)(e|E)(g|G)(i|I)(n|N))"
t_FECHA_CHAVES = "((e|E)(n|N)(d|D))"
t_REAL = "\d+\.?\d*|-\d+\.?\d*"
t_INICIALIZADOR = "((p|P)(r|R)(o|O)(g|G)(r|R)(a|A)(m|M))"
t_TIPO_DADO = integer+ "|"+ real +"|"+ boolean +"|"+ char +"|"+string
#t_IDENTIFICADOR = "[a-zA-Z]\w*"
t_ENTAO = "((t|T)(h|H)(e|E)(n|N))"
t_SE = "if | If | IF | iF"
t_IDENTIFICADOR = "(\w|_)(\w|\d|_)*" #Inicia com uma letra ou "_" seguido por letra ou numero ou "_"
t_SEPARADOR_CMD = ";"
t_SEPARADOR = ","
t_ignore = " \n"
t_ATRIBUICAO = ":="
t_TIPADOR = ":"
t_CONSTANTE_INTEIRA = "[0-9]\d*|-[1-9]\d*"
t_OPERADOR_ARITMETICO = "\+|\-|\*|\/"
t_PRINT = "(w|W)(r|R)(i|I)(t|T)(e|E)(l|L)(n|N)"
t_LEITOR = "(r|R)(e|E)(a|A)(d|D)(l|L)(n|N)"
t_ABRE_PARENTESES = "[(]"
t_FECHA_PARENTESES = "[)]"
t_ASPAS = "\'"
#sempre jogar os operadores com tamanho maior na frente caso
#aja uma repeticao de caractere neste caso <> e <
t_OPERADOR_RELACIONAL = "<>|>=|<=|=|>|<"
t_OPERADOR_LOGICO = "((a|A)(n|N)(d|D))|((n|N)(o|O)(t|T))|((o|O)(r|R))"
t_SENAO = "((e|E)(l|L)(s|S)(e|E))"
t_REPETICAOFOR = "((f|F)(o|O)(r|R))"
t_UPORDOWN = "(d|D)(o|O)(w|W)(n|N)(t|T)(o|O)|(t|T)(o|O)"
t_REPETICAOWHILE = "((w|W)(h|H)(i|I)(l|L)(e|E))"
t_DO = "DO | Do | dO | do"

'''Alfabeto case insensitive
(a|A)(b|B)(c|C)(d|D)(e|E)(f|F)(g|G)(h|H)(i|I)(j|J)(k|K)(l|L)(m|M)
(n|N)(o|O)(p|P)(q|Q)(r|R)(s|S)(t|T)(u|U)(v|V)(w|W)(x|X)(y|Y)(z|Z)
'''

#Regra, caso ocorra erro
def t_error(t):
    
    print(f'Illegal character {t.value[0]!r}')
    t.lexer.skip(1)
    #inicia aq " ''' "
    '''
    for i in t.value:
        if(i  != " "):
            l.skip(1)
            temp = i
        else:
            print(f"Token {temp} não definido na Linha {t.lineno}, posição {t.lexpos}")
            break

#Instanciar o lex
l = lex()
arquivo = open("Lexer\main.pascal","r")
#definir o texto de entrada
fita = arquivo.read()
#Carregar o lex
l.input(fita)

#Ler token a token
while True:
    t = l.token()
    #Se acabar a fita
    if not t:
        break
    
    print(t)
#fecha aq '''

class FHO_Lexer:
    def __init__(self, nome_arquivo):
        #Instanciar o lex
        self.l = lex()
        arquivo = open(nome_arquivo, "r")
        #Definir o texto entrada
        fita = arquivo.read()
        
        #Carregar no lex
        self.l.input(fita)
    
    def proximoToken(self):
        return self.l.token()
        
