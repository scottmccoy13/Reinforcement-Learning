# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        
        PSUEDO CODE FROM BOOK
        
        repeat:
          values = Uprime
          delta = 0
          for state in S:
            Uprime = reward + gamma * sum(probability * U[s'])
            if |Uprime[s] - values[s]| > delta:
              delta = |Uprime[s] - values[s]|
        until: delta < epsilon(1 - gamma)/gamma

        This qsuedocode was basically useless...
        The Bellman equation was somewhat helpful though. I watched several
        youtube videos and read slides and code snipets from other sources 
        to come up with this solution

        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        #a copy of the values of the states
        Uprime = self.values.copy()
        #need a finite number of passes large enough to converge
        for i in range(self.iterations):
          Uprime = self.values.copy() #first step in psuedocode loop
          for state in mdp.getStates():
            #state value is what the value of our state will be after convergence
            stateValue = None
            for action in self.mdp.getPossibleActions(state):
              #get the q values for the current state for every action
              currValue = self.computeQValueFromValues(state, action)
              #if we have null value for our state or if current value is
              #less than the currently observed transition then replace it
              if stateValue == None or stateValue < currValue:
                stateValue = currValue
            #if all of the currValues were null then assign a default 0
            if stateValue == None:
              stateValue = 0
            #update the value for the state
            Uprime[state] = stateValue
          self.values = Uprime.copy()

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        #Qvalue for the state in question
        Qvalue = 0
        #returns (state, probability) pair
        delta = self.mdp.getTransitionStatesAndProbs(state, action)

        #this part of code is basically representing the summation
        #from the Bellman equation
        #for every transition from the current
        sigma = 0
        for item in delta:
          reward = self.mdp.getReward(state, action, item[0])
          probability = item[1] 

          #R(s) 
          sigma += reward

          #R(s) + gamma * P(s' | s,a) * U[s']
          sigma += (self.discount * (probability * self.values[item[0]]))

          Qvalue += sigma
          sigma = 0

        return Qvalue

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        #if we are in terminal state then we must exit so no actions
        if self.mdp.isTerminal(state) == True:
          return None
        else:
          possibleAction = None
          possibleValue = None

          for action in self.mdp.getPossibleActions(state):
            #for every action check the possible states values and replace
            #our current best value and remember what action lead to it
            if self.computeQValueFromValues(state, action) >= possibleValue:
              possibleValue = self.computeQValueFromValues(state, action)
              possibleAction = action

            #this loop wont work the first time without this line
            if possibleValue == None:
              possibleValue = self.computeQValueFromValues(state, action)
              possibleAction = action

          return possibleAction

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
