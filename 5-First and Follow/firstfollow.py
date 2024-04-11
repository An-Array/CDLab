def compute_first(string, non_terminals, terminals, productions_dict):
    first_set = set()
    if string in non_terminals:
        for alternative in productions_dict[string]:
            first_set |= compute_first(alternative, non_terminals, terminals, productions_dict)
            if '@' not in compute_first(alternative, non_terminals, terminals, productions_dict):
                break
    elif string in terminals:
        first_set.add(string)
    elif string == '' or string == '@':
        first_set.add('@')
    else:
        first_set |= compute_first(string[0], non_terminals, terminals, productions_dict)
        if '@' in first_set:
            i = 1
            while '@' in first_set:
                first_set -= {'@'}
                if string[i:] in terminals:
                    first_set.add(string[i:])
                    break
                elif string[i:] == '':
                    first_set.add('@')
                    break
                first_set |= compute_first(string[i:], non_terminals, terminals, productions_dict)
                i += 1
    return first_set

  def compute_follow(nT, non_terminals, terminals, productions_dict, starting_symbol):
    follow_set = set()
    if nT == starting_symbol:
        follow_set.add('$')
    for nt, rhs in productions_dict.items():
        for alt in rhs:
            for char_index, char in enumerate(alt):
                if char == nT:
                    following_str = alt[char_index + 1:]
                    if following_str == '':
                        if nt != nT:
                            follow_set |= compute_follow(nt, non_terminals, terminals, productions_dict, starting_symbol)
                    else:
                        follow_set |= compute_first(following_str, non_terminals, terminals, productions_dict) - {'@'}
                        if '@' in compute_first(following_str, non_terminals, terminals, productions_dict):
                            follow_set |= compute_follow(nt, non_terminals, terminals, productions_dict, starting_symbol)
    return follow_set

  def main():
    no_of_terminals = int(input("Enter no. of terminals: "))
    terminals = [input("Enter terminal {}: ".format(i+1)) for i in range(no_of_terminals)]
    no_of_non_terminals = int(input("Enter no. of non terminals: "))
    non_terminals = [input("Enter non terminal {}: ".format(i+1)) for i in range(no_of_non_terminals)]
    starting_symbol = input("Enter the starting symbol: ")
    no_of_productions = int(input("Enter no of productions: "))
    productions = [input("Enter production {}: ".format(i+1)) for i in range(no_of_productions)]

    productions_dict = {non_terminal: [] for non_terminal in non_terminals}
    for production in productions:
        nonterm_to_prod = production.split("->")
        alternatives = nonterm_to_prod[1].split("/")
        for alternative in alternatives:
            productions_dict[nonterm_to_prod[0]].append(alternative)

    FIRST = {non_terminal: set() for non_terminal in non_terminals}
    for non_terminal in non_terminals:
        FIRST[non_terminal] |= compute_first(non_terminal, non_terminals, terminals, productions_dict)

    FOLLOW = {non_terminal: set() for non_terminal in non_terminals}
    FOLLOW[starting_symbol] |= {'$'}
    for non_terminal in non_terminals:
        FOLLOW[non_terminal] |= compute_follow(non_terminal, non_terminals, terminals, productions_dict, starting_symbol)

    print("{: ^20}{: ^20}{: ^20}".format('Non Terminals','First','Follow'))
    for non_terminal in non_terminals:
        print("{: ^20}{: ^20}{: ^20}".format(non_terminal, str(FIRST[non_terminal]), str(FOLLOW[non_terminal])))

  if __name__ == "__main__":
    main()
