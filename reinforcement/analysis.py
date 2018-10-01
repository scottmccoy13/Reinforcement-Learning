# analysis.py
# -----------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


######################
# ANALYSIS QUESTIONS #
######################

# Set the given parameters to obtain the specified policies through
# value iteration.

'''
Question 1 attempt 1
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        print self.values
        self.values = dict([(state, 0) for state in mdp.getStates()])
        Uprime = self.values.copy()

        for i in range(self.iterations):
          self.values = Uprime.copy()
          delta = 0
          vect = []
          fullvect = [] #vector of action, summation pairs
          for state in mdp.getStates():
            for action in mdp.getPossibleActions(state):
              for s_p in mdp.getTransitionStatesAndProbs(state, action):
                vect.append(s_p[1] * self.values[s_p[0]])
              fullvect.append( (action, sum(filter(None,vect))) )
              del vect[:]
            try:
              print action
              bestAction = ("north", 0.0)
              for item in fullvect:
                if item[1] > bestAction:
                  bestAction = item
            except:
              bestAction = ((0, 0), 0.0) #this should never be our final value
            Uprime[state] = self.discount * bestAction[1] #+ getReward(state, bestAction[0], )

'''

def question2():
    answerDiscount = 0.0
    answerNoise = 0.2
    return answerDiscount, answerNoise

def question3a():
    answerDiscount = 0.6
    answerNoise = 0.0
    answerLivingReward = -2.0
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3b():
    answerDiscount = 0.7
    answerNoise = 0.2
    answerLivingReward = -0.7
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3c():
    answerDiscount = 0.8
    answerNoise = 0.0
    answerLivingReward = -1.0
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3d():
    answerDiscount = 0.7
    answerNoise = 0.1
    answerLivingReward = -0.15
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3e():
    answerDiscount = 0.0
    answerNoise = 0.0
    answerLivingReward = 1.0
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question6():
    answerEpsilon = None
    answerLearningRate = None
    return answerEpsilon, answerLearningRate
    # If not possible, return 'NOT POSSIBLE'

if __name__ == '__main__':
    print 'Answers to analysis questions:'
    import analysis
    for q in [q for q in dir(analysis) if q.startswith('question')]:
        response = getattr(analysis, q)()
        print '  Question %s:\t%s' % (q, str(response))
