from gym import spaces
import numpy as np
import random
from itertools import groupby
from itertools import product
import copy



class TicTacToe():

    def __init__(self):
        """initialise the board"""
        
        # initialise state as an array
        self.state = [np.nan for _ in range(9)]  # initialises the board position, can initialise to an array or matrix
        # all possible numbers
        self.all_possible_numbers = [i for i in range(1, len(self.state) + 1)] # , can initialise to an array or matrix

        self.reset()


    def is_winning(self, curr_state):
        """Takes state as an input and returns whether any row, column or diagonal has winning sum
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan]
        Output = False"""
        if(((curr_state[0]+curr_state[1]+curr_state[2])==15) | ((curr_state[3]+curr_state[4]+curr_state[5])==15) |((curr_state[6]+curr_state[7]+curr_state[8])==15)):
            return True
        elif(((curr_state[0]+curr_state[3]+curr_state[6])==15) | ((curr_state[1]+curr_state[4]+curr_state[7])==15) |((curr_state[2]+curr_state[5]+curr_state[8])==15)):
            return True
        elif(((curr_state[0]+curr_state[4]+curr_state[8])==15) | ((curr_state[2]+curr_state[4]+curr_state[6])==15)):
            return True
        else:
            return False
 

    def terminal(self, curr_state):
        # Terminal state could be winning state or when the board is filled up

        if self.is_winning(curr_state) == True:
            return True, 'Win'

        elif len(self.allowed_positions(curr_state)) ==0:
            return True, 'Tie'

        else:
            return False, 'Resume'
        
    def who_wins(self,curr_action):
        if (curr_action[1]%2 != 0):
            return 10
        else:
            return -10


    def allowed_positions(self, curr_state):
        """Takes state as an input and returns all indexes that are blank"""
        return [i for i, val in enumerate(curr_state) if np.isnan(val)]


    def allowed_values(self, curr_state):
        """Takes the current state as input and returns all possible (unused) values that can be placed on the board"""

        used_values = [val for val in curr_state if not np.isnan(val)]
        agent_values = [val for val in self.all_possible_numbers if val not in used_values and val % 2 !=0]
        env_values = [val for val in self.all_possible_numbers if val not in used_values and val % 2 ==0]

        return (agent_values, env_values)


    def action_space(self, curr_state):
        """Takes the current state as input and returns all possible actions, i.e, all combinations of allowed positions and allowed values"""

        agent_actions = product(self.allowed_positions(curr_state), self.allowed_values(curr_state)[0])
        env_actions = product(self.allowed_positions(curr_state), self.allowed_values(curr_state)[1])
        return (agent_actions, env_actions)



    def statetransition(self, curr_state, curr_action):
        """Takes current state and action and returns the board position just after agent's move.
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan], action- [7, 9] or [position, value]
        Output = [1, 2, 3, 4, nan, nan, nan, 9, nan]
        """
        new_state = copy.deepcopy(curr_state)
        new_state[curr_action[0]]=curr_action[1]
        return new_state


    def step(self, curr_state, curr_action):
        """Getting agent next move, check whether it is terminal state or not, randomly move environment and again check for terminal state. Here copy ensures that the current state is not modified."""
        new_state=self.statetransition(curr_state, curr_action)
        k,v=self.terminal(new_state)
        if ((k==True) & (v=="Win")):
            r=self.who_wins(curr_action)
        elif ((k==True) & (v=="Tie")):
            r=0
        else:
            position = random.choice(self.allowed_positions(new_state))
            value = random.choice(self.allowed_values(new_state)[1])
            new_state[position]=value
            k,v=self.terminal(new_state)
            if ((k==True) & (v=="Win")):
                r=self.who_wins(curr_action)
            elif ((k==True) & (v=="Tie")):
                r=0
            else:
                r=-1
        return new_state,r,k 
        
    def reset(self):
        return self.state
