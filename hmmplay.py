#!/usr/bin/python3

import random

def rndstate(states):
    r = random.random()
    limit = 0.0
    for s in states:
        limit += states[s]
        if r < limit:
            return s

def viterbi(obs, states, start_probability, transitions, emission):
    V = [{}]
    for st in states:
        V[0][st] = {"prob": start_probability[st] * emission[st][obs[0]], "prev": None}
    for t in range(1, len(obs)):
        V.append({})
        for st in states:
            max_tr_prob = max(V[t-1][prev_st]["prob"] * transitions[prev_st][st] for prev_st in states)
            for prev_st in states:
                if V[t-1][prev_st]["prob"] * transitions[prev_st][st] == max_tr_prob:
                    max_prob = max_tr_prob * emission[st][obs[t]]
                    V[t][st] = {"prob": max_prob, "prev": prev_st}
                    break
    opt = []
    max_prob = max(value["prob"] for value in V[-1].values())
    previous = None
    for st, data in V[-1].items():
        if data["prob"] == max_prob:
            opt.append(st)
            previous = st
            break
    for t in range(len(V) - 2, -1, -1):
        opt.insert(0, V[t+1][previous]["prev"])
        previous = V[t+1][previous]["prev"]

    return(opt, max_prob)

states = ('rainy', 'sunny')
observations = ('walk', 'shop', 'clean')

start_probability = {'rainy': 0.6, 'sunny': 0.4}

transition_probability = {
        'rainy': {'rainy': 0.7, 'sunny': 0.3},
        'sunny': {'rainy': 0.4, 'sunny': 0.6}
        }

emission_probability = {
        'rainy': {'walk': 0.1, 'shop': 0.4, 'clean': 0.5},
        'sunny': {'walk': 0.6, 'shop': 0.3, 'clean': 0.1}
        }

hidden_state = rndstate(start_probability)

obs = list()
real = list()
for i in range(100):
    hidden_state = rndstate(transition_probability[hidden_state])
    obs_state    = rndstate(emission_probability[hidden_state])
    obs.append(obs_state)
    real.append(hidden_state)
    #print(hidden_state, obs_state, sep = "\t")

hidden, mp = viterbi(obs, states, start_probability, transition_probability, emission_probability)

for i in range(len(obs)):
    if hidden[i] != real[i]:
        msg = "Fok"
    else:
        msg = ""
    print(obs[i], hidden[i], real[i], msg, sep = "\t")
print(mp)
