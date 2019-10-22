"""
Contains tests for the GraphPartitioning class.
"""

from qcware.optimization.problems import GraphPartitioning
from qcware.optimization.utils import solve_qubo_bruteforce, solve_ising_bruteforce
from numpy import allclose


edges = {("a", "b"), ("a", "c"), ("c", "d"),
         ("b", "c"), ("e", "f"), ("d", "e")}
problem = GraphPartitioning(edges)
solutions = (
    ({"a", "b", "c"}, {"d", "e", "f"}),
    ({"d", "e", "f"}, {"a", "b", "c"})
)

problem_weighted = GraphPartitioning({(0, 1): 1, (1, 2): 3, (0, 3): 1})
solutions_weighted = (
    ({0, 3}, {1, 2}),
    ({1, 2}, {0, 3})
)


def test_graphpartitioning_str():

    assert eval(str(problem)) == problem


def test_graphpartitioning_properties():

    assert problem.E == edges
    problem.V
    problem.degree
    problem.weights


def test_graphpartitioning_bruteforce():

    assert problem.solve_bruteforce() in solutions
    assert (
        problem.solve_bruteforce(all_solutions=True) in
        (list(solutions), list(reversed(solutions)))
    )


# QUBO

def test_graphpartitioning_qubo_solve():

    e, sol = solve_qubo_bruteforce(problem.to_qubo())
    solution = problem.convert_solution(sol)

    assert solution in solutions
    assert problem.is_solution_valid(solution)
    assert problem.is_solution_valid(sol)
    assert allclose(e, 1)

    e, sol = solve_qubo_bruteforce(problem_weighted.to_qubo())
    solution = problem_weighted.convert_solution(sol)

    assert solution in solutions_weighted
    assert problem_weighted.is_solution_valid(solution)
    assert problem_weighted.is_solution_valid(sol)
    assert allclose(e, 1)


def test_graphpartitioning_qubo_numvars():

    Q = problem.to_qubo()
    assert (
        len(set(y for x in Q for y in x)) ==
        problem.num_binary_variables ==
        Q.num_binary_variables
    )


# ising

def test_graphpartitioning_ising_solve():

    e, sol = solve_ising_bruteforce(problem.to_ising())
    solution = problem.convert_solution(sol)

    assert solution in solutions
    assert problem.is_solution_valid(solution)
    assert problem.is_solution_valid(sol)
    assert allclose(e, 1)

    e, sol = solve_ising_bruteforce(problem_weighted.to_ising())
    solution = problem_weighted.convert_solution(sol)

    assert solution in solutions_weighted
    assert problem_weighted.is_solution_valid(solution)
    assert problem_weighted.is_solution_valid(sol)
    assert allclose(e, 1)


def test_graphpartitioning_ising_numvars():

    L = problem.to_ising()
    assert L.num_binary_variables == problem.num_binary_variables
