"""
@author: Daniel Willhelm
"""

from scipy.stats import multinomial
from typing import List, Tuple 
import numpy as np
import warnings

class MarkovSequence:
    """A Markov sequence generator class.
    
    Notes
    -----
    Most of the code here is derived from the reference below. Please refer there for 
    more details on this implimentation of Markov sequences.

    https://ericmjl.github.io/essays-on-data-science/machine-learning/markov-models/
    
    """
    def __init__(self, states:List[str], transition_matrix:np.ndarray) -> None:
        """Markov sequence generator.

        Parameters
        ----------
        states : List[str]
            A list of possible states. 
        transition_matrix : np.ndarray
            The transition matrix which describes the probabilities of transitioning to 
            one state to another. Should be of shape (n_states, n_states).
        """
        self.states = states
        self.transition_matrix = transition_matrix
        self._validate(states, transition_matrix) 

        self.state_mapper = {key:value for key,value in enumerate(states)}

    def get_sequence(self, sequence_len:int, init_state:str=None) -> Tuple[str, ...]:
        """Generate a Markov sequence from a given sequence length and initial state.

        Parameters
        ----------
        sequence_len : int
            The length of the Markov sequence.
        init_state : str, optional
            The initial state use to seed the Markov sequence, by default None. If None,
            the initial state is determined from transition matrix. 
        """
        # sanity check for user input for init state
        if init_state is not None and init_state not in self.states: 
            msg = f"{init_state=} was not found in the knowns states: {self.states=}"
            raise ValueError(msg)
        
        # set up the initial probability vector
        if init_state is None: 
            p_vec = self.equilibrium_distribution(self.transition_matrix)
        else: 
            p_vec = np.zeros(shape=len(self.states))
            p_vec[self.states.index(init_state)] = 1

        # init the markov sequence
        initial_state = list(multinomial.rvs(1, p_vec)).index(1)

        sequence = [initial_state]
        for _ in range(sequence_len - 1): 
            p_vec = self.transition_matrix[sequence[-1]]
            sequence.append(list(multinomial.rvs(1, p_vec)).index(1))
        
        # map states to state IDs
        sequence = list(map(self.state_mapper.get, sequence))
        return tuple(sequence) 

    def equilibrium_distribution(self, transition_matrix:np.ndarray) -> np.ndarray:
        """Calculate the equilibrium distribution from a transition matrix."""
        n_states = transition_matrix.shape[0]
        A = np.append(
            arr=transition_matrix.T - np.eye(n_states),
            values=np.ones(n_states).reshape(1, -1),
            axis=0
        )
        # Moore-Penrose pseudo-inverse = (A^TA)^{-1}A^T
        pinv = np.linalg.pinv(A)
        # Return last row
        return pinv.T[-1]

    def _validate(self, states:List[str], transition_matrix:np.ndarray):
        """Add some sanity checks to input values.""" 
        if (len(states), len(states)) != transition_matrix.shape: 
            msg = "Please ensure that the transition matrix is of shape (n_states, n_states)" 
            raise ValueError(msg)

        ones = np.ones(len(states))
        if not all(np.isclose(transition_matrix.sum(axis=1), ones)): 
            msg = "The probabilities should sum to ~1.0 (over rows)"
            raise ValueError(msg)


class DummyMarkovSequence(MarkovSequence): 

    def __init__(self, states: List[str], transition_matrix: np.ndarray) -> None:
        super().__init__(states, transition_matrix)
        warnings.warn("WARNING: You are using a dummy markov sequence which is non-stocastic.")
    
    def get_sequence(self, sequence_len: int, init_state: str = None) -> Tuple[str, ...]:
        sequence = ["Q1", "Q2", "Q3", "Q4", "NMA", "HF"]
        if len(sequence) < sequence_len: 
            sequence = sequence + ["Q1"] * (sequence_len - len(sequence))
        elif len(sequence) > sequence_len: 
            sequence = sequence[:sequence_len]
        return sequence


if __name__ == '__main__':
    # NOTE: this is probably the most basic "unit-test" one can set up, but its better 
    # than nothing. You can test the code by calling the module directly - `python markov.py`

    # use example
    _states = ["Q1", "Q2", "Q3", "Q4", "NMA", "HF"]
    _transition_matrix = np.array([
        [0.4,0.05,0.4,0.05,0.05,0.05],
        [0.3,0.05,0.25,0.2,0.1,0.1],
        [0.3,0.1,0.3,0.14,0.08,0.08],
        [0.3,0.05,0.3,0.25,0.05,0.05],
        [0.2,0.15,0.2,0.4,0.025,0.025],
        [0.21,0.13,0.13,0.13,0.28,0.12]
    ])

    foo = MarkovSequence(states=_states, transition_matrix=_transition_matrix)
    sequence = foo.get_sequence(5, "Q1")
    print(sequence)
    
    # how to use dummy markov class 
    bar = DummyMarkovSequence(states=_states, transition_matrix=_transition_matrix)
    sequence = bar.get_sequence(8)
    print(sequence)



