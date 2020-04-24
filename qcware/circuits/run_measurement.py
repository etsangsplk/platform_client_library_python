#  AUTO-GENERATED FILE - MODIFY AT OWN RISK
#  Project: qcware
#  Copyright (c) 2019 QC Ware Corp - All Rights Reserved


  
import numpy
  
from quasar import Circuit
  
from .. import logger
from ..api_calls import post_call, wait_for_call, handle_result
from ..util.transforms import client_args_to_wire
  


def run_measurement(backend:str=None, circuit:Circuit=None, nmeasurement:int=None, statevector:numpy.ndarray=None, min_qubit:int=None, nqubit:int=None, dtype:type=numpy.complex128, backend_args:object={}, api_key:str=None, host:str=None):
    r"""Executes a Quasar circuit multiple times, measuring the resulting statevector for a histogram of probabilities. This is possibly best used via the QuasarBackend class, which provides a number of extensions.

Arguments:

:param backend: A string representing the backend for execution
:type backend: str

:param circuit: The circuit to execute
:type circuit: Circuit

:param nmeasurement: The number of measurements required
:type nmeasurement: int

:param statevector: If the  backend supports statevector input, this provides an initial state.
:type statevector: numpy.ndarray

:param min_qubit: The minimum occupied qubit index
:type min_qubit: int

:param nqubit: The total number of qubit indices in the circuit
:type nqubit: int

:param dtype: For some backends, particularly simulators, the type used to represent the statevector
:type dtype: type

:param backend_args: Any extra parameters to pass to the backend
:type backend_args: object


:return: A quasar ProbabilityHistogram object representing the histogram of states measured during execution
:rtype: quasar.ProbabilityHistogram
    """
    data = client_args_to_wire('circuits.run_measurement', **locals())
    api_call = post_call('circuits/run_measurement', data, host=host )
    logger.info(f'API call to circuits.run_measurement successful. Your API token is {api_call["uid"]}')
    return handle_result(wait_for_call(api_key=api_key,
                                       host=host,
                                       call_token=api_call['uid']))
