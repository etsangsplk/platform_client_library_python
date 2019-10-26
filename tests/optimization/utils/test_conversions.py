"""
Contains tests for the QUBO/PUBO to/from Ising/HIsing functions.
"""

from qcware.optimization.utils import (
    qubo_to_ising, ising_to_qubo, pubo_to_hising, hising_to_pubo,
    binary_to_spin, spin_to_binary, decimal_to_binary, decimal_to_spin,
    qubo_to_matrix, matrix_to_qubo, binary_to_decimal, spin_to_decimal
)
from qcware.optimization import QUBO, Ising, PUBO, HIsing
from sympy import Symbol
import numpy as np
from numpy.testing import assert_raises


def test_qubo_to_ising_to_qubo():

    qubo = {(0,): 1, (0, 1): 1, (1,): -1, (1, 2): .2, (): -2, (2,): 1}
    assert qubo == ising_to_qubo(qubo_to_ising(qubo))

    qubo = {('0',): 1, ('0', 1): 1, (1,): -1, (1, '2'): .2, (): -2, ('2',): 1}
    # need to reformatt qubo so it is sorted with the same hash
    assert QUBO(qubo) == ising_to_qubo(qubo_to_ising(qubo))


def test_ising_to_qubo_to_ising():

    ising = {(0, 1): -4, (0, 2): 3, (): -2, (0,): 1, (2,): -2}
    assert ising == qubo_to_ising(ising_to_qubo(ising))

    ising = {('0', 1): -4, ('0', '2'): 3, (): -2, ('0',): 1, ('2',): -2}
    # need to reformat ising so it is sorted with the same hash
    assert Ising(ising) == qubo_to_ising(ising_to_qubo(ising))


def test_pubo_to_hising_to_pubo():

    pubo = {
        (0,): 1, (0, 1): 1, (1,): -1, (1, 2): .5, (): -2, (2,): 1,
        (0, 2, 3): -3, (0, 1, 2): -2
    }
    assert pubo == hising_to_pubo(pubo_to_hising(pubo))

    pubo = {
        ('0',): 1, ('0', 1): 1, (1,): -1, (1, '2'): .5, (): -2, ('2',): 1,
        ('0', '2', 3): -3, ('0', 1, '2'): -2
    }
    # need to reformat pubo so it is sorted with the same hash
    assert PUBO(pubo) == hising_to_pubo(pubo_to_hising(pubo))


def test_hising_to_pubo_to_hising():

    hising = {
        (0, 1): -4, (0, 2): 3, (): -2, (0,): 1, (2,): -2,
        (0, 1, 2): 3, (0, 2, 3): -1
    }
    assert hising == pubo_to_hising(hising_to_pubo(hising))

    hising = {
        ('0', 1): -4, ('0', '2'): 3, (): -2, ('0',): 1, ('2',): -2,
        ('0', 1, '2'): 3, ('0', '2', 3): -1
    }
    # need to reformat qubo so it is sorted with the same hash
    assert HIsing(hising) == pubo_to_hising(hising_to_pubo(hising))


def test_qubo_to_ising_eq_pubo_to_hising():

    qubo = {(0,): 1, (0, 1): 1, (1,): -1, (1, 2): .2, (): -2, (2,): 1}
    assert qubo_to_ising(qubo) == pubo_to_hising(qubo)


def test_ising_to_qubo_eq_hising_to_pubo():

    ising = {(0, 1): -4, (0, 2): 3, (): -2, (0,): 1, (2,): -2}
    assert ising_to_qubo(ising) == hising_to_pubo(ising)


def test_decimal_to_binary():

    assert decimal_to_binary(10, 7) == (0, 0, 0, 1, 0, 1, 0)
    assert decimal_to_binary(10) == (1, 0, 1, 0)

    with assert_raises(ValueError):
        decimal_to_binary(.5)

    with assert_raises(ValueError):
        decimal_to_binary(1000, 2)


def test_decimal_to_spin():

    assert decimal_to_spin(10, 7) == (-1, -1, -1, 1, -1, 1, -1)
    assert decimal_to_spin(10) == (1, -1, 1, -1)


def test_binary_to_decimal():

    for i in range(8):
        assert i == binary_to_decimal(decimal_to_binary(i))


def test_spin_to_decimal():

    for i in range(8):
        assert i == spin_to_decimal(decimal_to_spin(i))


def test_binary_to_spin():

    assert binary_to_spin(0) == -1
    assert binary_to_spin(1) == 1
    assert binary_to_spin((0, 1)) == (-1, 1)
    assert binary_to_spin([0, 1]) == [-1, 1]
    assert binary_to_spin({"a": 0, "b": 1}) == {"a": -1, "b": 1}


def test_spin_to_binary():

    assert spin_to_binary(-1) == 0
    assert spin_to_binary(1) == 1
    assert spin_to_binary((-1, 1)) == (0, 1)
    assert spin_to_binary([-1, 1]) == [0, 1]
    assert spin_to_binary({"a": -1, "b": 1}) == {"a": 0, "b": 1}


def test_matrix_to_qubo():

    matrix, qubo = [[-3, 1], [-1, 2]], {(0,): -3, (1,): 2}
    assert matrix_to_qubo(matrix) == qubo

    with assert_raises(ValueError):
        matrix_to_qubo([[1, 2, 3], [1, 0, 1]])


def test_qubo_to_matrix():

    matrix, qubo = [[-3, 1], [0, 2]], {(0, 0): -3, (0, 1): 1, (1, 1): 2}
    assert matrix == qubo_to_matrix(qubo, array=False)
    assert np.all(np.array(matrix) == qubo_to_matrix(qubo))

    matrix = [[-3, .5], [.5, 2]]
    assert matrix == qubo_to_matrix(qubo, array=False, symmetric=True)
    assert np.all(np.array(matrix) == qubo_to_matrix(qubo, symmetric=True))

    with assert_raises(ValueError):
        qubo_to_matrix({})

    with assert_raises(ValueError):
        qubo_to_matrix({(): 1, (0,): -1})


def test_symbols():

    a, b = Symbol('a'), Symbol('b')
    ising = {(0,): a, (0, 1): 1, (1,): -a, (1, 2): 1, (): -2*b, (2,): a}
    assert ising == qubo_to_ising(ising_to_qubo(ising))

    a, b = Symbol('a'), Symbol('b')
    qubo = {(0,): a, (0, 1): 1, (1,): -a, (1, 2): 1, (): -2*b, (2,): a}
    assert qubo == ising_to_qubo(qubo_to_ising(qubo))
