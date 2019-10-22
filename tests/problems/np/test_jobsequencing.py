"""
Contains tests for the JobSequencing class.
"""

from qcware.optimization.problems import JobSequencing
from qcware.optimization.utils import solve_qubo_bruteforce, solve_ising_bruteforce
from numpy import allclose


job_lengths = {"job1": 2, "job2": 3, "job3": 1}
num_workers = 2
problem = JobSequencing(job_lengths, num_workers, log_trick=False)
problem_log = JobSequencing(job_lengths, num_workers)
Q = problem.to_qubo()
Q_log = problem_log.to_qubo()
L = problem.to_ising()
L_log = problem_log.to_ising()

solutions = ({'job1', 'job3'}, {'job2'}), ({'job2'}, {'job1', 'job3'})
obj_val = 3


def test_jobsequencing_str():

    assert eval(str(problem)) == problem
    assert eval(str(problem_log)) == problem_log


def test_jobsequencing_properties():

    x, m = (2, 1, 2), 2
    p = JobSequencing(x, m)
    assert p.job_lengths == x
    assert p.num_workers == m
    assert p.log_trick
    p.M


def test_jobsequencing_bruteforce():

    assert problem.solve_bruteforce() in solutions
    assert (
        problem.solve_bruteforce(all_solutions=True) in
        (list(solutions), list(reversed(solutions)))
    )


def test_jobsequencing_bruteforce_solve():

    assert problem.solve_bruteforce() in solutions
    assert problem.solve_bruteforce(True) in (
        list(solutions), [solutions[1], solutions[0]]
    )


# QUBO

def test_jobsequencing_qubo_logtrick_solve():

    e, sol = solve_qubo_bruteforce(Q_log)
    solution = problem_log.convert_solution(sol)
    assert problem_log.is_solution_valid(solution)
    assert problem_log.is_solution_valid(sol)
    assert solution in solutions
    assert allclose(e, obj_val)


def test_jobsequencing_qubo_solve():

    e, sol = solve_qubo_bruteforce(Q)
    solution = problem.convert_solution(sol)
    assert problem.is_solution_valid(solution)
    assert problem.is_solution_valid(sol)
    assert solution in solutions
    assert allclose(e, obj_val)


def test_jobsequencing_qubo_logtrick_numvars():

    assert (
        len(set(y for x in Q_log for y in x)) ==
        problem_log.num_binary_variables ==
        Q_log.num_binary_variables
    )


def test_jobsequencing_qubo_numvars():

    assert (
        len(set(y for x in Q for y in x)) ==
        problem.num_binary_variables ==
        Q.num_binary_variables
    )


# ising

def test_jobsequencing_ising_logtrick_solve():

    e, sol = solve_ising_bruteforce(L_log)
    solution = problem_log.convert_solution(sol)
    assert problem_log.is_solution_valid(solution)
    assert problem_log.is_solution_valid(sol)
    assert solution in solutions
    assert allclose(e, obj_val)


def test_jobsequencing_ising_solve():

    e, sol = solve_ising_bruteforce(L)
    solution = problem.convert_solution(sol)
    assert problem.is_solution_valid(solution)
    assert problem.is_solution_valid(sol)
    assert solution in solutions
    assert allclose(e, obj_val)


def test_jobsequencing_ising_logtrick_numvars():

    assert L_log.num_binary_variables == problem_log.num_binary_variables


def test_jobsequencing_ising_numvars():

    assert L.num_binary_variables == problem.num_binary_variables
