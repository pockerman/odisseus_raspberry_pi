echo "PYTHONPATH ${PYTHONPATH}"
PYTHONPATH=$PYTHONPATH:${PWD}
python3 tests/test_propulsion.py
