Higher Order Ising Optimization (HOIO)
=======================================

Accessed with ``qcware.optimization.HOIO``. Note that it is important to use the ``HOIO.convert_solution`` function to convert solutions of the PUBO, QUBO, Hising or Ising formulations of the HOIO back to a solution to the HOIO formulation.

We also discuss the ``qcware.optimization.spin_var`` function here, which is just returns a ``HOIO``.


.. autoclass:: qcware.optimization.HOIO
    :members:


.. autofunction:: qcware.optimization.spin_var
