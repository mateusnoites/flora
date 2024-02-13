import sys

def separar(texto, separador_abre, separador_fecha):
    novo_texto = (texto.strip().split(separador_abre, 1)[1].split(separador_fecha, 1)[0]).strip()
    return novo_texto

def definir_tipo(variavel):
    variavel = variavel.strip()
    if variavel.startswith('"') and variavel.endswith('"'):
        tipo = "texto"
    elif variavel.isdigit():
        tipo = "numero"
    else:
        tipo = "desconhecido"
    
    return tipo

class FloraInterpreter:
    def __init__(self):
        self.variables = {}

    def interpret(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()

            for line in lines:
                line = line.strip()
                if line:
                    self.execute(line)
    
    def variavel(self, linha):
        valor_variavel = linha.split('->')[1].strip()
        nome_variavel = separar(linha.split('->')[0].strip(), '(', ')')
        tipo_variavel = definir_tipo(valor_variavel)

        if tipo_variavel == "texto":
            valor_variavel = separar(valor_variavel.strip(), '"', '"')
        
        self.variables[nome_variavel] = f'->{valor_variavel}<- tipo="{tipo_variavel}"'

    def escreva(self, linha):
        argumento = linha.split('->')[1].strip()
        texto_escrito = ""

        if argumento in self.variables:
            valor_memoria = self.variables[argumento]
            valor = separar(valor_memoria, '->', '<-')
            tipo = separar(valor_memoria, 'tipo="', '"')

            if tipo == 'texto':
                texto_escrito = valor.strip('"')
            elif tipo == 'numero':
                texto_escrito = valor
            else:
                print(f'O valor que você tentou escrever possui o tipo: {tipo}. Portanto, ele não pôde ser escrito.')
                return
        elif '"' in argumento:
            argumento = argumento.strip('"')
            texto_escrito = argumento
        elif argumento.isdigit():
            texto_escrito = argumento
        else:
            print(f'O valor que você tentou escrever possui o tipo: desconhecido. Portanto, ele não pôde ser escrito.')
            return

        print(texto_escrito)
        

    def execute(self, line):
        palavras = line.strip().split()

        if palavras:
            if palavras[0].startswith("var(") or palavras[0].startswith("variavel("):
                self.variavel(line)
            elif palavras[0].startswith("escreva"):
                self.escreva(line)

interpreter = FloraInterpreter()

if len(sys.argv) == 2:
    interpreter.interpret(sys.argv[1])
elif len(sys.argv) < 2:
    arquivo = input("Qual é o caminho do arquivo Flora deve ser executado? ")
    interpreter.interpret(arquivo)
else:
    print("Uso: flora seu_arquivo.flora")
