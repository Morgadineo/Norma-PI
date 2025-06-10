from os import ST_NOATIME


class NormaCode:

    def __init__(self, filename: str) -> None:
        self.filename  : str = filename
        self.registers : dict[str, int] = dict()
        self.labels    : dict[str, tuple] = dict()

        self.execute_code()

    def execute_code(self):
        """
        Método para executar o código armazenado dentro da classe.
        """
        self.read_code()

        first_line = str(next(iter(self.labels.keys())))

        running = self.execute_line(first_line)

        while running != None:
            running = self.execute_line(running)

    def execute_line(self, label: str):
        """
        Método para executar a instrução armazenada na linha rotulada por
        label.

        :param label: Rótulo da linha a ser executada.
        """
        command, register, goto_1, goto_2 = self.labels[label]

        if self.execute_command(label, command, register) in (1, None):
            return self.goto(goto_1)
        else:
            return self.goto(goto_2)

    def goto(self, label: str):
        """
        Método para ir para uma determinada label.

        :param label: Label que representa uma linha.
        """
        if label in self.labels.keys():
            return label
        else:
            print("FIM DO PROGRAMA")
            return None

    def execute_command(self, label:str, command: str, reg: str):
        """
        Executa o comando passado utilizando o registrador reg.

        :param command: Comando como 'zero', 'add' e 'dec'
        :param reg: Registrador a ser utilizado.

        :return: None caso o comando não seja zero REG
                 0 caso zero REG seja verdadeiro.
                 1 caso zero REG seja falso.

        """
        match command:

            case "add":
                self.add(reg)
            
            case "dec":
                self.dec(reg)

            case "zero":
                return self.if_zero(reg)

        #######################################################################
        # Exibição dos registradores
        #
        # Ignora esse menu bizarro.
        # Ainda estou desenvolvendo o menu utilizando o Tkinter.
        #######################################################################

        print(f"{label}:{command}{reg}", end="")
        regs_n = 0
        for reg in self.registers:
            print(f"\t{reg}", end="")
            regs_n += 1
        print(f"\n", end="")

        for value in self.registers.values():
            print(f"\t{value}", end="")
        print(f"\n---------{'--------' * (regs_n - 1)}--")
        return None

    def parse_line(self, line: str) -> tuple[str, str, str, str, str | None]:
        """
        Método para analisar uma linha/instrução da máquina norma.
        
        :param line: A linha a ser analisada.
        """
        line = line.strip()
        splitted_line: list[str] = line.split(" ")
        tag     : str = splitted_line[0][:-1]
        sttmt   : str = splitted_line[1]
        command : str = splitted_line[2]
        register: str = splitted_line[3]
        goto_1  : str = splitted_line[6]
        goto_2  : str | None = None

        if sttmt == "if":
            goto_2 = splitted_line[9]
        else:
            goto_1 : str = splitted_line[6]

        return tag, command, register, goto_1, goto_2

    def create_reg(self, register: str):
        """
        Método para criar um registrar caso ele não exista.

        :param register: O nome do registrador a ser criado.
        """
        if not register in self.registers.keys():
            self.registers.update({register: 0})

    def dec(self, register: str):
        """
        Método próprio da máquina Norma para decrementar 1 a um registrador.
        
        :param register: O nome do regitrado a ser decrementado.
        """
        self.create_reg(register)

        self.registers[register] -= 1
        
    def add(self, register: str):
        """
        Método próprio da máquina Norma para adicionar 1 a um registrador.

        :param register: O nome do registrador a ser somado.
        """
        self.create_reg(register)

        self.registers[register] += 1

    def create_intruct(self, line: tuple[str, str, str, str, str | None]):
        """
        Método para criar uma instrução no dicionário label.
        A instrução é um par chave-valor, sendo a chave uma label e valor
        uma 4-tupla com as especificações de comando, registrador e próxima
        label.
        """
        instruct: tuple[str, str, str, str | None] = (line[1], line[2], line[3], line[4])
        self.labels.update({line[0]: instruct})

    def read_code(self):
        """
        Método para ler um código fonte de uma máquina Norma.

        :param filename: Nome do arquivo a ser lido.
        """
        with open(self.filename, "r") as file:
            content: list[str] = [line for line in file.readlines() if len(line) > 1]
            for line in content:
                parsed_line: tuple[str, str, str, str, str | None] = self.parse_line(line)
                self.create_intruct(parsed_line)

    def if_zero(self, register: str):
        """
        Função própria da máquina Norma para verificar se um determinado
        registrador armazena o valor zero. 

        :param register: Nome do registrador a ser verificado.
        
        """
        self.create_reg(register)

        if self.registers[register] == 0:
            return 1

        return 0

if __name__ == "__main__":
    norma = NormaCode("./menorQue.txt")
