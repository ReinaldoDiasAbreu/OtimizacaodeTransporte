'''
Código Criado por: Michael Stott
Disponível em: https://github.com/MichaelStott/SimplexSolver
'''

import ast, getopt, sys, copy, os
from fractions import Fraction

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

class SimplexSolver():
    ''' Solves linear programs using simplex algorithm and
        output problem steps in LaTeX file.
    '''

    # Table for converting inequality list to LaTeX    
    latex_ineq = {'=': '=',
                  '<=': r'\leq',
                  '>=': r'\geq'}

    def __init__(self):
        self.A = []
        self.b = []
        self.c = []
        self.t = []
        self.tableau = []
        self.entering = []
        self.departing = []
        self.ineq = []
        self.prob = "min"
        self.gen_doc = False
        self.doc = ""
        self.f = 0
        self.s = 0

    def run_simplex(self, A, b, c, f, s, t, prob='min', ineq=[],
                    enable_msg=False, latex=False):
        ''' Run simplex algorithm.'''
        self.prob = prob
        self.gen_doc = latex  #Criar ou nao o doc
        self.ineq = ineq
        self.s = s
        self.f = f
        self.t = t
        # Add slack & artificial variables
        self.set_simplex_input(A, b, c)
            
        # Are there any negative elements on the bottom (disregarding
        # right-most element...)
        while (not self.should_terminate()):            
            # Attempt to find a non-negative pivot.
            pivot = self.find_pivot()
            # Do row operations to make every other element in column zero.
            self.pivot(pivot)  
        solution = self.get_current_solution()  # Obtem a solucao
        self.doc_generate(solution)
        return solution

    def set_simplex_input(self, A, b, c):
        ''' Set initial variables and create tableau.'''
        # Convert all entries to fractions for readability.
        for a in A:
            self.A.append([Fraction(x) for x in a])    
        self.b = [Fraction(x) for x in b]
        self.c = [Fraction(x) for x in c]
        if not self.ineq:
            if self.prob == 'max':
                self.ineq = ['<='] * len(b)
            elif self.prob == 'min':
                self.ineq = ['<='] * len(b)   # Alteração
            
        self.update_enter_depart(self.get_Ab())

        # If this is a minimization problem...
        if self.prob == 'min':
            # ... find the dual maximum and solve that.
            m = self.get_Ab()
            m.append(self.c + [0])
            m = [list(t) for t in zip(*m)] # Calculates the transpose
            self.A = [x[:(len(x)-1)] for x in m]
            self.b = [y[len(y) - 1] for y in m]
            self.c = m[len(m) -1]
            self.A.pop()
            self.b.pop()
            self.c.pop()
            self.ineq = ['<='] * len(self.b)

        self.create_tableau()
        self.ineq = ['='] * len(self.b)
        self.update_enter_depart(self.tableau)

    def update_enter_depart(self, matrix):
        self.entering = []
        self.departing = []
        # Create tables for entering and departing variables
        for i in range(0, len(matrix[0])):
            if i < len(self.A[0]):
                prefix = 'x' if self.prob == 'max' else 'y'
                self.entering.append("%s_%s" % (prefix, str(i + 1)))
            elif i < len(matrix[0]) - 1:
                self.entering.append("s_%s" % str(i + 1 - len(self.A[0])))
                self.departing.append("s_%s" % str(i + 1 - len(self.A[0])))
            else:
                self.entering.append("b")

    def add_slack_variables(self):
        ''' Add slack & artificial variables to matrix A to transform
            all inequalities to equalities.
        '''
        slack_vars = self._generate_identity(len(self.tableau))
        for i in range(0, len(slack_vars)):
            self.tableau[i] += slack_vars[i]
            self.tableau[i] += [self.b[i]]

    def create_tableau(self):
        ''' Create initial tableau table.
        '''
        self.tableau = copy.deepcopy(self.A)
        self.add_slack_variables()
        c = copy.deepcopy(self.c)
        for index, value in enumerate(c):
            c[index] = -value
        self.tableau.append(c + [0] * (len(self.b)+1))

    def find_pivot(self):
        ''' Find pivot index.'''
        enter_index = self.get_entering_var()
        depart_index = self.get_departing_var(enter_index)
        return [enter_index, depart_index]

    def pivot(self, pivot_index):
        ''' Perform operations on pivot.'''
        j,i = pivot_index

        pivot = self.tableau[i][j]
        self.tableau[i] = [element / pivot for
                           element in self.tableau[i]]
        for index, row in enumerate(self.tableau):
           if index != i:
              row_scale = [y * self.tableau[index][j]
                          for y in self.tableau[i]]
              self.tableau[index] = [x - y for x,y in
                                     zip(self.tableau[index],
                                         row_scale)]

        self.departing[i] = self.entering[j]
        
    def get_entering_var(self):
        ''' Get entering variable by determining the 'most negative'
            element of the bottom row.'''
        bottom_row = self.tableau[len(self.tableau) - 1]
        most_neg_ind = 0
        most_neg = bottom_row[most_neg_ind]
        for index, value in enumerate(bottom_row):
            if value < most_neg:
                most_neg = value
                most_neg_ind = index
        return most_neg_ind   

    def get_departing_var(self, entering_index):
        ''' To calculate the departing variable, get the minimum of the ratio
            of b (b_i) to the corresponding value in the entering collumn. 
        '''
        skip = 0
        min_ratio_index = -1
        min_ratio = 0
        for index, x in enumerate(self.tableau):
            if x[entering_index] != 0 and x[len(x)-1]/x[entering_index] > 0:
                skip = index
                min_ratio_index = index
                min_ratio = x[len(x)-1]/x[entering_index]
                break
        
        if min_ratio > 0:
            for index, x in enumerate(self.tableau):
                if index > skip and x[entering_index] > 0:
                    ratio = x[len(x)-1]/x[entering_index]
                    if min_ratio > ratio:
                        min_ratio = ratio
                        min_ratio_index = index
        
        return min_ratio_index

    def get_Ab(self):
        ''' Get A matrix with b vector appended.'''
        matrix = copy.deepcopy(self.A)
        for i in range(0, len(matrix)):
            matrix[i] += [self.b[i]]
        return matrix

    def should_terminate(self):
        ''' Determines whether there are any negative elements
            on the bottom row '''
        result = True
        index = len(self.tableau) - 1
        for i, x in enumerate(self.tableau[index]):
            if x < 0 and i != len(self.tableau[index]) - 1:
                result = False
        return result

    def get_current_solution(self):
        ''' Get the current solution from tableau. '''
        solution = {}
        for x in self.entering:
            if x is not 'b':
                if x in self.departing:
                    solution[x] = self.tableau[self.departing.index(x)]\
                                  [len(self.tableau[self.departing.index(x)])-1]
                else:
                    solution[x] = 0
        solution['z'] = self.tableau[len(self.tableau) - 1]\
                          [len(self.tableau[0]) - 1]
        
        # If this is a minimization problem...
        if (self.prob == 'min'):
            # ... then get x_1, ..., x_n  from last element of
            # the slack columns.
            bottom_row = self.tableau[len(self.tableau) - 1]
            for v in self.entering:
                if 's' in v:
                    solution[v.replace('s', 'x')] = bottom_row[self.entering.index(v)]    
        
        return solution
    
    def _fraction_to_latex(self, fract):
        if fract.denominator == 1:
            return str(fract.numerator)
        else:
            return r"\frac{%s}{%s}" % (str(fract.numerator), str(fract.denominator))

    def _generate_identity(self, n):
        ''' Helper function for generating a square identity matrix.
        '''
        I = []
        for i in range(0, n):
            row = []
            for j in range(0, n):
                if i == j:
                    row.append(1)
                else:
                    row.append(0)
            I.append(row)
        return I

    def doc_generate(self, solution):
        # Cria tabela de envio e gera o documento latex
        if not self.gen_doc:
            return
        self.doc = (r"\documentclass{article}"
                    r"\usepackage[utf8]{inputenc}"
                    r"\title{Relatório de Entregas}"
                    r"\author{Reinaldo J. Dias de Abreu e Mirralis Dias Santana}"
                    r"\date{\today}"
                    r"\begin{document}"
                    r"\maketitle"
                    r"\subsection*{Tabela de Entregas}"
        )

        # Removendo valores de X na solucao
        x = list([])
        for i in range(1,len(self.b)+1):
            x.append(solution['x_'+str(i)])

        # Organizando os valores em uma tabela farmacia x cliente
        c1 = 0
        c2 = 1
        table = list([])
        for i in range(int(self.f)):
            table.append(x[c1:(int(self.s))*c2])
            c1 += int(self.s)
            c2 += 1

        # Imprime tabela de solução
        print("Farmácia    Quant   Cliente")
        custo = 0
        for i in range(int(self.f)):
            for j in range(int(self.s)):
                if table[i][j] != 0: # Se envio zero, nao exibe
                    if j == int(self.s)-1 and (int(self.s) > int(self.f)): # Caso exesso estoque, cliente 0
                        print("%5.0f     %5.0f    %5.0f" %(i+1, table[i][j], 0))
                    elif i == 0 and (int(self.f) > int(self.s)): # Caso falta estoque, farmacia -1
                        print("%5.0f     %5.0f    %5.0f" %(-(i+1), table[i][j], j+1))
                    else:
                        print("%5.0f     %5.0f    %5.0f" %(i+1, table[i][j], j+1))
                        custo += self.t[i][j] # Calcula o custo real de envio
        
        print("\n Custo Total : " , custo)

        # Cria a mesma tabela no documento latex
        self.doc += (r"\begin{table}[!hb]\centering\begin{tabular}{|c|c|c|}\hline Farmácia  & Quantidade & Cliente\\ \hline")
        for i in range(int(self.f)):
            for j in range(int(self.s)):
                if table[i][j] != 0:
                    if j == int(self.s)-1 and (int(self.s) > int(self.f)):
                        self.doc += (r"%5.0f  &   %5.0f  &  %5.0f \\" %(i+1, table[i][j],0))
                    elif i == 0 and (int(self.f) > int(self.s)):
                        self.doc += (r"%5.0f  &   %5.0f  &  %5.0f \\" %(-(i+1), table[i][j],j+1))
                    else:
                        self.doc += (r"%5.0f  &   %5.0f  &  %5.0f \\" %(i+1, table[i][j],j+1))
        self.doc += (r"\hline\end{tabular}\end{table}")

        self.doc += (r"\subsubsection*{Custo Total: %10.5f}" %(custo))
        self.doc += (r"\begin{quote}Observações:\begin{itemize}"
                    r"\item Caso farmácia indique -1, significa que há falta de estoque disponível para envio ao cliente."
                    r"\item Caso cliente indique 0, significa que há excesso de estoque que não precisa ser enviado."
                    r"\end{itemize}\end{quote}"
                    )

        # Finaliza Documento
        self.doc += (r"\end{document}")
        with open("solution.tex", "w") as tex:
            tex.write(self.doc)

                    
if __name__ == '__main__':
    clear()

    ''' COMMAND LINE INPUT HANDLING '''
    A = []
    b = []
    c = []
    t = []
    p = ''
    f = 0
    s = 0
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv,"hA:b:c:p:t:f:s",["A=","b=","c=","p=","t=","f=","s="])
        
    except getopt.GetoptError:
        print('simplex.py -A <matrix> -b <vector> -c <vector> -p <type>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('simplex.py -A <matrix> -b <vector> -c <vector> -p <obj_func_type>')
            print('A: Matrix that represents coefficients of constraints.')
            print('b: Ax <= b')
            print('c: Coefficients of objective function.')
            print('p: Indicates max or min objective function.')
            sys.exit()
        elif opt in ("-A"):
            A = ast.literal_eval(arg)
        elif opt in ("-b"):
            b = ast.literal_eval(arg)
        elif opt in ("-c"):
            c = ast.literal_eval(arg)
        elif opt in ("-t"):
            t = ast.literal_eval(arg)
        elif opt in ("-p"):
            p = arg.strip()
        elif opt in ("-f"):
            f = arg.strip()
        elif opt in ("-s"):
            s = arg.strip()
    
    s = int(argv[13])
        
    if not A or not b or not c:
        print('Must provide arguments for A, b, c (use -h for more info)')
        sys.exit()
    ''' END OF COMMAND LINE INPUT HANDLING '''
    
    if p not in ('max', 'min'):
        p = 'min'

    
    SimplexSolver().run_simplex(A, b, c, f, s, t, prob=p, ineq=[], enable_msg=False, latex=True)
