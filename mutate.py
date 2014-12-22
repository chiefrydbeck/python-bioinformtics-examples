#Function that takes a string as input, chooses a random position, and exchanges the symbol at that location according to probabilities of a given dict.
#We can than apply this function iteratively to a string, and see what we get. We can also apply it very many times, to see whether it then converges towards a given string (or not).
#We can provide two different substitution matrices - one that converges to only a single symbol, and one that diverges, but only with two (or three) different nucleotides.

# The rate at which  mutations occur at a given position in the genome depends on the nucleotide at the postion but maybe more importantly at the surrounding sequence context.
#There are a number of reason why the observed mutation rates betwen differnet nucleides vary. One is that there are differnet mechansism generating transition from one base to another.
#Another is that the efficientcy of the repair mechansim, which is extensive precess in living divideng cells, vary for different nucleotides. The surrounding context of the position determines to what degree
#there is a working selelection pressure. 

####Mutation example

import random

def mutate(dna):
    dna_nmer_list = list(dna)
    mutation_site = random.randint(0, len(dna_nmer_list) - 1)
    possible_mutations = list('ATCG')
    possible_mutations.remove(dna[mutation_site])
    dna_nmer_list[mutation_site] = random.choice(possible_mutations)
    return ''.join(dna_nmer_list)

def print_freqs(dna):
    for base in 'AGCT':
       print 'Frequency of %s = %s' % (base, dna.count(base)*1.0/len(dna))

dna = 'ACGGAGATTTCGGTATGCAT'

print 'Starting DNA: ' + dna
print_freqs(dna)

for i in range(10000):
    dna = mutate(dna)

print 'Mutated DNA: ' + dna
print_freqs(dna)

def create_random_markov_chain():
    markov = {}
    for from_base in 'ACGT':
       slice_points = sorted([0] + [random.random() for i in range(3)] + [1])
       transition_probs = [slice_points[i+1] - slice_points[i] for i in range(4)]
       markov[from_base] = dict([ (to_base, prob) for to_base, prob in zip('ACGT', transition_probs) ])
    return markov
   
markov = create_random_markov_chain()
print markov
print markov['A']['T']

def print_transition_probs(markov):
    for to_base in 'ACGT':
       print 'Sum of probabilities for transition to %s = %s' % \
           (to_base, sum(markov[from_base][to_base] for from_base in 'ACGT')/4.0)

print_transition_probs(markov)


def select_to_base(possible_base_transitions):
    rand_0_1 = random.random()
    for to_base, transition_prob in possible_base_transitions:
       if rand_0_1 < transition_prob:
           break
       rand_0_1 = rand_0_1 - transition_prob
    return to_base

def mutate_markov(dna, markov):
    dna_nmer_list = list(dna)
    mutation_site = random.randint(0, len(dna_nmer_list) - 1)
    from_base = dna[mutation_site]
    possible_base_transitions = markov[from_base].items()
    dna_nmer_list[mutation_site] = select_to_base( possible_base_transitions )
    return ''.join(dna_nmer_list)

markov = create_random_markov_chain()
print markov
print_transition_probs(markov)

dna = 'ACGGAGATTTCGGTATGCAT'
print 'Starting DNA: ' + dna
print_freqs(dna)

for j in range(1000):
    dna = mutate_markov(dna, markov)

print 'Mutated DNA: ' + dna
print_freqs(dna)
