from automata.fa.dfa import DFA
from automata.fa.nfa import NFA

def q2a():
    return '1'

def q2b(a, b):
    states = set()
    transitions = {}
    final_states = set()
    input_symbols = a.input_symbols.union(b.input_symbols)
    
    # For dfa duplication
    for s in a.states:
        a_s = f"A_{s}"
        states.add(a_s)
    
    for curr, trans in a.transitions.items():
        a_curr = f"A_{curr}"
        if a_curr not in transitions:
            transitions[a_curr] = {}

        for sym, nxt in trans.items():
            a_nxt = f"A_{nxt}"
            transitions[a_curr][sym] = {a_nxt}

    a_init = f"A_{a.initial_state}"
    init_state = a_init

    for f in a.final_states:
        a_f = f"A_{f}"
        final_states.add(a_f)

    # Epislon from a to b
    for i, a_state in enumerate(a.states):
        for s in b.states:
            b_s = f"B{i}_{s}"
            states.add(b_s)

        for curr, trans in b.transitions.items():
            b_curr = f"B{i}_{curr}"
            if b_curr not in transitions:
                transitions[b_curr] = {}

            for sym, nxt in trans.items():
                b_nxt = f"B{i}_{nxt}"
                transitions[b_curr][sym] = {b_nxt}

        a_curr = f"A_{a_state}"
        b_init = f"B{i}_{b.initial_state}"

        if a_curr not in transitions:
            transitions[a_curr] = {}

        if '' not in transitions[a_curr]:
            transitions[a_curr][''] = set()

        transitions[a_curr][''].add(b_init)
        
        # Epsilon transition back
        for j, b_f in enumerate(b.final_states):
            for s in a.states:
                ret_a_s = f"C{i}{j}_{s}"
                states.add(ret_a_s)

            for curr, trans in a.transitions.items():
                ret_a_curr = f"C{i}{j}_{curr}"
                if ret_a_curr not in transitions:
                    transitions[ret_a_curr] = {}

                for sym, nxt in trans.items():
                    ret_a_nxt = f"C{i}{j}_{nxt}"
                    transitions[ret_a_curr][sym] = {ret_a_nxt}

            b_f_state = f"B{i}_{b_f}"
            ret_target = f"C{i}{j}_{a_state}"

            if b_f_state not in transitions:
                transitions[b_f_state] = {}

            if '' not in transitions[b_f_state]:
                transitions[b_f_state][''] = set()

            transitions[b_f_state][''].add(ret_target)

            for f in a.final_states:
                ret_a_f = f"C{i}{j}_{f}"
                final_states.add(ret_a_f)
    
    # Injected NFA from a and b
    injected_nfa = NFA(
        input_symbols = input_symbols,
        states = states,
        transitions = transitions,
        initial_state = init_state,
        final_states = final_states
    )

    return injected_nfa
