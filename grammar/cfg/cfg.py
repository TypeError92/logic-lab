class CFG:
    def __init__(
            self,
            variables: set[str],
            terminals: set[str],
            production_rules: dict[str, set[tuple[str]]],
            starting_symbol: str
    ):
        self.variables = variables
        self.terminals = terminals
        self.production_rules = production_rules
        self.starting_symbol = starting_symbol

    @classmethod
    def from_bnf_file(cls, filename: str) -> 'CFG':
        with open(filename, encoding='utf', mode='rt') as file:
            return cls.from_bnf_str(file.read())

    @classmethod
    def from_bnf_str(cls, bnf_str: str) -> 'CFG':
        # TODO: Parse bnf notation and return a CFG.
        pass

    def to_cnf(self) -> 'CFG':
        """Returns a new equivalent CFG object with the production rules converted to Chomsky normal form."""

        # 1. START: Eliminate the start symbol from right-hand sides
        new_starting_symbol = '<START>'  # TODO: Ensure that this symbol is not used yet
        new_variables = {*self.variables, new_starting_symbol}
        new_production_rules = {new_starting_symbol: {(self.starting_symbol,)}}

        # 2. TERM: Eliminate rules with nonsolitary terminals
        for (left, right) in self.production_rules.items():
            new_right = set()
            for alternative in right:
                if len(alternative) > 1:
                    new_alternative = []
                    for symbol in alternative:
                        if symbol in self.terminals:
                            associated_variable = f'<TERM({symbol})>'
                            if associated_variable not in new_variables:
                                new_variables.add(associated_variable)
                                new_production_rules[associated_variable] = {(symbol,)}
                            new_alternative.append(associated_variable)
                        else:
                            new_alternative.append(symbol)
                    new_right.add(tuple(new_alternative))
                else:
                    new_right.add(alternative)
            new_production_rules[left] = new_right

        # 3. BIN: Eliminate right-hand sides with more than 2 nonterminals

        # 4. DEL: Eliminate ε-rules

        # 5. UNIT: Eliminate unit rules

        return CFG(new_variables, self.terminals, new_production_rules, new_starting_symbol)


if __name__ == '__main__':
    """
     Example (https://en.wikipedia.org/wiki/Chomsky_normal_form#Example):
     Expr 	→ Term 	| Expr AddOp Term 	| AddOp Term
     Term 	→ Factor 	| Term MulOp Factor
     Factor 	→ Primary 	| Factor ^ Primary
     Primary 	→ 1 	| x 	| ( Expr ) # reduced for simplicity
     AddOp 	→ + 	| −
     MulOp 	→ * 	| / 
     """

    grammar = CFG(
        variables={'<expr>', '<term>', '<factor>', '<primary>', '<add-op>', '<mul-op>'},
        terminals={'^', '2', 'x', '(', ')', '+', '-', '*', '/'},
        production_rules={
            '<expr>': {
                ('<term>',),
                ('<expr>', '<add-op>', '<term>'),
                ('<add-op', '<term>')
            },
            '<term>': {
                ('<factor>',),
                ('<term>', '<mul-op>', '<factor>')
            },
            '<factor>': {
                ('<primary>',),
                ('<factor>', '^', '<primary>')
            },
            '<primary>': {
                ('1',),
                ('x',),
                ('(', '<expr>', ')')
            },
            '<add-op>': {
                ('+',),
                ('-',)
            },
            '<mul-op>': {
                ('*',),
                ('/',)
            }
        },
        starting_symbol='<expr>'
    )

    normalized_grammar = grammar.to_cnf()
    for item in normalized_grammar.production_rules.items():
        print(item)