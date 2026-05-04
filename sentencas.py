import itertools
from sympy import symbols, Not
from sympy.logic.boolalg import to_cnf, to_dnf, simplify_logic
from sympy.logic.inference import satisfiable

# 0. Configurando as variáveis proposicionais (átomos)
P, Q, R= symbols('P Q R')

# (i.1) Verificar equivalência usando Tabela Verdade

def eq_tabela_verdade(expr1, expr2, variaveis):

    # Gera todas as combinações (V, V), (V, F), (F, V), (F, F)...
    combinacoes = list(itertools.product([True, False], repeat=len(variaveis)))
    
    for valores in combinacoes:
        # Cria um dicionário mapeando cada variável para True ou False
        mapeamento = dict(zip(variaveis, valores))
        
        # Substitui as variáveis pelos valores booleanos e avalia a sentença
        resultado1 = expr1.subs(mapeamento)
        resultado2 = expr2.subs(mapeamento)
        
        # Se divergir em qualquer linha da tabela verdade, não são equivalentes
        if resultado1 != resultado2:
            return False
            
    return True


# (i.2) Verificar equivalência algebricamente

def eq_algebrica(expr1, expr2):
    
##De Morgan, Distributiva 
    return simplify_logic(expr1) == simplify_logic(expr2)


# (ii) Gerar fnc

def gerar_fnc(expr):
    """
    Converte para Produto de Somas (FNC).
    """
    return to_cnf(expr)

# (iii) Gerar fnd

def gerar_fnd(expr):
    """
    Converte para Soma de Produtos (FND).
    """
    return to_dnf(expr)


# (iv) Verificar se é satisfatível (SAT Solver)

def verificar_sat(expr):
    """
    Retorna False se for uma contradição (insatisfatível).
    Se for satisfatível, retorna um modelo (exemplo de valores que tornam a sentença Verdadeira).
    """
    resultado = satisfiable(expr)
    if resultado is False:
        return False, "Insatisfatível (Contradição)"
    return True, resultado

# (v) Verificar se uma é a negação da outra
def eh_negacao(expr1, expr2):
    """
    Simplifica a primeira expressão e compara com a simplificação da negação da segunda.
    """
    return simplify_logic(expr1) == simplify_logic(Not(expr2))


# Exemplos práticos
if __name__ == "__main__":
    # Vamos usar duas sentenças equivalentes clássicas (Lei de De Morgan)
    # S1: ~(P | Q)     -> Não (P ou Q)
    # S2: ~P & ~Q      -> Não P e Não Q
    sentenca_A = ~(P | Q)
    sentenca_B = ~P & ~Q
    
    # Sentença para testes de FNC/FND e SAT
    sentenca_C = (P >> Q) & (Q >> R)  # Se P então Q, e se Q então R
    
    print("=== TESTES DO SISTEMA ===")
    
    # i.1
    print(f"\n(i.1) S1 e S2 são equivalentes por Tabela Verdade? {eq_tabela_verdade(sentenca_A, sentenca_B, [P, Q])}")
    
    # i.2
    print(f"(i.2) S1 e S2 são equivalentes Algebricamente? {eq_algebrica(sentenca_A, sentenca_B)}")
    
    # ii e iii
    print(f"\nSentença Original: {sentenca_C}")
    fnc_c = gerar_fnc(sentenca_C)
    print(f"(ii) Forma Normal Conjuntiva (FNC): {fnc_c}")
    print(f"(iii) Forma Normal Disjuntiva (FND): {gerar_fnd(sentenca_C)}")
    
    # iv
    is_sat, modelo = verificar_sat(fnc_c)
    print(f"\n(iv) A sentença gerada em (ii) é satisfatível? {is_sat}")
    if is_sat:
        print(f"     Valores que satisfazem (Modelo SAT): {modelo}")
        
    # v
    sentenca_D = P & Q
    sentenca_E = ~(P & Q)
    print(f"\n(v) A sentença 'D' é negação de 'E'? {eh_negacao(sentenca_D, sentenca_E)}")