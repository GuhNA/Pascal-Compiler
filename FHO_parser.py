from Pascal_lexer import FHO_Lexer
import sys
import re

class FHO_Parser:
    
    def __init__(self, nome_arquivo):
        self.l = FHO_Lexer(nome_arquivo)
        self.lookAhead = self.l.proximoToken()
        self.varPassou = False
        self.constPassou = False
        self.OnIf = False
        
    def erro(self, mensagem):
        print("Erro sintatico! ", mensagem)
        sys.exit(1)
        
    def match(self, esperado):
        if self.lookAhead == None:
            self.erro("Final do arquivo")
            sys.exit(1)

        if esperado == self.lookAhead.type:
            self.lookAhead = self.l.proximoToken()
        else:
            self.erro("Esperado: " + esperado + "\nencontrado: " + self.lookAhead.type + ": " 
                    +self.lookAhead.value + "\nlinha: "+str(self.lookAhead.lineno)+", coluna: "+str(self.lookAhead.lexpos))
            sys.exit(1)
            

            
    #Programa -> program x ;
    
    def Programa(self):
        self.match("INICIALIZADOR")
        self.match("IDENTIFICADOR")
        self.match("SEPARADOR_CMD")        

        for i in range(2):
            #const
            if self.lookAhead.type == "QUALIFICADORCONST":
                if not self.constPassou:
                    self.match("QUALIFICADORCONST")
                    self.ConstVar()
                else:
                    self.erro("Const já foi instanciado!")
                    sys.exit(1)
            #var
            if self.lookAhead.type == "QUALIFICADORVAR":
                if not self.varPassou:
                    self.match("QUALIFICADORVAR")
                    self.Declaracao()
                else:
                    self.erro("Var já foi instanciado!")
                    sys.exit(1)

        #begin
        self.match("ABRE_CHAVES")
        self.Corpo()
        #end
        self.match("FECHA_CHAVES")
    #Corpo -> Atribuicao
    #Atribuicao -> id := Expressao_inicial ;
    def Atribuicao(self, onIf):
            #Necessario ONIF pois em casos de else é necessario que o separadorCMD não exista
            #E em casos de if sem begin e end, podemos utilizar ou não ";"
            self.match("IDENTIFICADOR")
            self.match("ATRIBUICAO")
            self.ExpressaoInicial()
            if onIf == 'nao':
                self.match("SEPARADOR_CMD")
            elif onIf == 'double':
                if self.lookAhead.type == "SEPARADOR_CMD":
                    self.match("SEPARADOR_CMD")

    def Texto(self):
        self.lookAhead = self.l.proximoToken()
        while self.lookAhead.type != "ASPAS":
            if self.lookAhead.value == None:
                self.erro("Esperado \"'\"")
                sys.exit(1)
            self.lookAhead = self.l.proximoToken()
        self.lookAhead = self.l.proximoToken()

    #CORPO_WRITE -> 'TEXTO' | expressaoInicial | 'TEXTO ' , expressaoInicial EXPRESSAO_TEXTO
    def CorpoWrite(self):
        if self.lookAhead.type == "ASPAS":
            self.Texto()
        if self.lookAhead.type == "SEPARADOR":
            self.match("SEPARADOR")
            self.ExpressaoInicial()
            self.ExpressaoTexto()

    #EXPRESSAO_TEXTO -> , 'TEXTO'| , 'TEXTO' , ExpressaoInicial EXPRESSAO_TEXTO| $
    def ExpressaoTexto(self):
        if self.lookAhead.type == "SEPARADOR":
            self.match("SEPARADOR")
            if self.lookAhead.type == "ASPAS": 
                self.Texto()
            else:
                self.erro("Esperado \"'\" nao encontrado")
                sys.exit(1)
            if self.lookAhead.type == "SEPARADOR":
                self.match("SEPARADOR")
                self.ExpressaoInicial()
                self.ExpressaoTexto()
    
    #INSTRUCAO -> Atribuicao | writeln(CORPO_WRITE) | readLn(id)
    def Instrucao(self, onIf):
        if self.lookAhead.type == "IDENTIFICADOR":
            self.Atribuicao(onIf)
        elif self.lookAhead.type == "PRINT":
            self.match("PRINT")
            self.match("ABRE_PARENTESES")
            self.CorpoWrite()
            self.match("FECHA_PARENTESES")
        elif self.lookAhead.type == "LEITOR":
            self.match("LEITOR")
            self.match("ABRE_PARENTESES")
            self.match("IDENTIFICADOR")
            self.match("FECHA_PARENTESES")
        else:
            print("ERRO! ESPERADO UMA INSTRUCAO")
            sys.exit(1)

    def Corpo(self):
        if self.lookAhead.type == "SE":
            self.IFElse()
            self.Corpo()
        if self.lookAhead.type == "IDENTIFICADOR":
            self.Atribuicao('nao')
            self.Corpo()
        if self.lookAhead.type == "REPETICAOFOR":
            self.CorpoFor()
    
    # "for" IDENTIFICADOR ":=" FATOR "downto/to" FATOR do
    def CorpoFor(self):
        self.match("REPETICAOFOR")
        self.match("IDENTIFICADOR")
        self.match("ATRIBUICAO")
        self.Fator()
        self.match("UPORDOWN")
        self.Fator()
        self.match("DO")
        if self.lookAhead.type == "ABRE_CHAVES":
            self.match("ABRE_CHAVES")
            self.Corpo()
            self.match("FECHA_CHAVES")
        else:
            self.Instrucao('double')


    #Expressao Inicial -> Termo_Inicial Expressao
    def ExpressaoInicial(self):
        self.TermoInicial()
        self.Expressao()

    #Expressao -> + Termo_Inicial Expressao | - Termo_Inicial Expressao | $
    def Expressao(self):
        if self.lookAhead.value == "+" or self.lookAhead.value == "-":
            self.match("OPERADOR_ARITMETICO")
            self.TermoInicial()
            self.Expressao()

        #Termo Inicial -> Fator Termo
    def TermoInicial(self):
        self.Fator()
        self.Termo()
    
    #Termo -> * Fator Termo | / Fator Termo | $
    def Termo(self):
        if self.lookAhead.value == "*" or self.lookAhead.value == "/":
            self.match("OPERADOR_ARITMETICO")
            self.Fator()
            self.Termo()

    #Fator -> id, cte, ( Expressão )
    def Fator(self):
        if self.lookAhead.type == "IDENTIFICADOR":
            self.match("IDENTIFICADOR")
        elif self.lookAhead.type == "CONSTANTE_INTEIRA":
            self.match("CONSTANTE_INTEIRA")
        elif self.lookAhead.type == "REAL":
            self.match("REAL")
        elif self.lookAhead.type == "ABRE_PARENTESES":
            self.match("ABRE_PARENTESES")
            self.Expressao()
            self.match("FECHA_PARENTESES")
        else:
           self.erro("Esperado um fator!\n"+self.lookAhead.value +
                      "\nlinha: "+str(self.lookAhead.lineno)+", coluna: "
                      +str(self.lookAhead.lexpos))
           sys.exit(1)

    #Expressao Condicional -> E_I Op.Relacional E_I
    def ExpressaoCondicional(self):
        self.ExpressaoInicial()
        self.match("OPERADOR_RELACIONAL")
        self.ExpressaoInicial()


    #Expressao Condicional com operadores Logicos:
    # Op.R ( EXPRESSAO_CONDICIONAL ) ExpCondLogicos| $
    def ExpCondLogicos(self):
        if (self.lookAhead.type == "OPERADOR_LOGICO" and
            re.search("((n|N)(o|O)(t|T))", self.lookAhead.value) == None):
            self.match("OPERADOR_LOGICO")
            #Verifica casos de NOT em todas possibilidades
            if re.search("((n|N)(o|O)(t|T))", self.lookAhead.value) != None:
                self.match("OPERADOR_LOGICO")
            self.match("ABRE_PARENTESES")
            self.ExpressaoCondicional()
            self.match("FECHA_PARENTESES")
            self.ExpCondLogicos()
    ''' if not (A = B) and not (B <> C + 1) and (C > D) then
        if ( B = A + C ) and ( NomeAluno1 <> NomeAluno2 ) then
        if A <> B then '''
    #CASOS_IF -> not ( ExpressaoCondicional ) ExpCondLogicos | 
    # ( ExpressaoCondicional ) ExpCondLogicos| ExpressaoCondicional | $
    def CasosIf(self):
        if re.search("((n|N)(o|O)(t|T))", self.lookAhead.value) != None:
            self.match("OPERADOR_LOGICO")
            self.match("ABRE_PARENTESES")
            self.ExpressaoCondicional()
            self.match("FECHA_PARENTESES")
            self.ExpCondLogicos()

        elif self.lookAhead.value == "(":
            self.match("ABRE_PARENTESES")
            self.ExpressaoCondicional()
            self.match("FECHA_PARENTESES")
            self.ExpCondLogicos()

        elif(self.lookAhead.type == "IDENTIFICADOR"
        or  self.lookAhead.type == "CONSTANTE_INTEIRA"
        or  self.lookAhead.type == "REAL"):
            self.ExpressaoCondicional()


    def IFElse(self):
        self.match("SE")
        self.CasosIf()
        self.match("ENTAO")
        if self.lookAhead.type == "ABRE_CHAVES":
            self.match("ABRE_CHAVES")
            self.Corpo()
            self.match("FECHA_CHAVES")
        else:
            self.Instrucao('double')
        self.OnIf = True
        if self.lookAhead.type == "SENAO" and self.OnIf == True:
            self.match("SENAO")
            self.OnIf = False
            if self.lookAhead.type == "ABRE_CHAVES":
                self.match("ABRE_CHAVES")
                self.Corpo()
                self.match("FECHA_CHAVES")
            else : 
                self.Instrucao('double')
        if self.lookAhead.type == "SENAO" and self.OnIf != True:
            print("Nao e possivel iniciar else sem \"if\"\n"+self.lookAhead.value + "\nlinha: "
                  +str(self.lookAhead.lineno)+", coluna: "+str(self.lookAhead.lexpos))
            sys.exit(1)


    #Declaração -> id MaisVar : tipo; Declaração | $
    def Declaracao(self):
        #Obriga entrar primeira vez
        if not self.varPassou:
            self.match("IDENTIFICADOR")
            self.MaisVar()
            self.match("TIPADOR")
            self.match("TIPO_DADO")
            self.match("SEPARADOR_CMD")
            self.varPassou = True
            self.Declaracao()
        elif self.lookAhead.type == "IDENTIFICADOR":
            self.match("IDENTIFICADOR")
            self.MaisVar()
            self.match("TIPADOR")
            self.match("TIPO_DADO")
            self.match("SEPARADOR_CMD")

    #MaisVar -> , id MaisVar| $
    def MaisVar(self):
        if self.lookAhead.type == "SEPARADOR":
            self.match("SEPARADOR")
            self.match("IDENTIFICADOR")
            self.MaisVar()


    #ConstVar -> id = cte; ConstVar | $
    def ConstVar(self):
        #Obriga entrar primeira vez
        if not self.constPassou:
            self.match("IDENTIFICADOR")
            self.match("OPERADOR_RELACIONAL")
            if self.lookAhead.type == "IDENTIFICADOR":
                self.match("IDENTIFICADOR")
            elif self.lookAhead.type == "CONSTANTE_INTEIRA":
                self.match("CONSTANTE_INTEIRA")
            elif self.lookAhead.type == "REAL":
                self.match("REAL")
            self.match("SEPARADOR_CMD")
            self.constPassou = True
            self.ConstVar()
        elif self.lookAhead.type == "IDENTIFICADOR":
            self.match("IDENTIFICADOR")
            self.match("OPERADOR_RELACIONAL")
            self.ConstVar()

        

