
import unittest           # python testing framework
from ctypes import *      # python library for working with C
from pathlib import Path  # object oriented filesystem paths
import sys                # modifying import path
import secrets            # for generating cryptographically secure random numbers


submodule_dir_path = Path(__file__).resolve().parent.parent / 'keccak'  # Keccak submodule directory path - python implementation
submodule_dir_path = submodule_dir_path.resolve().absolute()            # Converts submodule dir path to absolute path
sys.path.append(str(submodule_dir_path))                                # Adds submodule dir to pythons import search paths
import keccak as keccak_py                                              # Imports keccak.py from submodule dir


base_path = Path(__file__).resolve().parent # base directory path
so_file = base_path / '../keccak.so'        # Keccak shared object - direct file path
keccak_c = CDLL(str(so_file))               # Loads shared object file using ctypes




# Create Array of random states for testing
def generate_random_states(num=3):
  states = []
  for i in range(num):
    # create array of 25 random 64-bit ints to populate state
    state = [secrets.randbits(64) for _ in range(25)]
    states.append(state)
  return states 
    

# Transforms array of 25 values to 5*5 C matrix
def transform_to_c_state(values):
  row = c_uint64 * 5      # Define row type (5 elements of uint64) using lib c_types  
  c_state = (row * 5)()   # Instantiate 5*5 matrix with c_row - all elements are set to zero  
  
  for x in range(5):      # Populate c_state with random values
    for y in range(5):
      c_state[x][y] = values[x * 5 + y]
  return c_state 


# Transforms array of 25 values to 5*5 Python matrix 
def transform_to_py_state(values):
  # Initialise state with 'keccakState' object from keccak.py file
  keccak_state = keccak_py.KeccakState(1088, 1600) # bitrate 1088, b=1600

  # Populate keccak_state.s matrix values
  for x in range(5):
    for y in range(5):
      keccak_state.s[x][y] = values[x * 5 + y]
  return keccak_state



class TestKeccakMethods(unittest.TestCase):

  def test_keccak_f(self):
    states = generate_random_states(3) # generates 3 random states for testing
    test_results = []

    for state in states:
      # Insantiate states
      c_state = transform_to_c_state(state) 
      py_state = transform_to_py_state(state)

      # Call keccak_f
      keccak_c.keccak_f(c_state)
      keccak_py.keccak_f(py_state)

      # Extract state 's' from keccak_py 
      py_result = py_state.s

      # Convert c_state to python list for fair comparison
      c_result = []
      for x in range(5):
        row = []
        for y in range(5):
          row.append(c_state[x][y])
        c_result.append(row)

      # Print Results
      print(f"C Result: \n{c_result}")
      print(f"Python Result: \n{py_result}")

      # Tests
      test_results.append((c_result == py_result))
      self.assertEqual(c_result, py_result, "C and Python results should be the same")
    
    print("================================ Keccak-f: Test Results ", test_results)
      



if __name__== '__main__':
  unittest.main()

















  # # check functions accessible from keccak.c
  # def test_ctypes(self): 
  #   keccak_c.add.restype = c_int            # returns int
  #   keccak_c.add.argtypes = [c_int, c_int]  # takes two ints as args

  #   # Call keccak add function
  #   result = keccak_c.add(6, 4)
  #   self.assertEqual(result, 10, "keccak_c.add(6, 4) should return 10")

  #   result = keccak_c.add(-2, 5)
  #   self.assertEqual(result, 3, "keccak_c.add(-2, 5) should return 3")

  #   result = keccak_c.add(0, 0)
  #   self.assertEqual(result, 0, "keccak_c.add(0, 0) should return 0")


  # # check functions accessible from keccak.py
  # def test_python_submodule(self):

  #   result = keccak_python.bits2bytes(15)
  #   self.assertEqual(result, 2.75, "Keccak_python.bits2bytes(15) should return 2.75")

  #   result = keccak_python.bits2bytes(8)
  #   self.assertEqual(result, 1.875, "Keccak_python.bits2bytes(15) should return 1.875")

  #   result = keccak_python.bits2bytes(0)
  #   self.assertEqual(result, 0.875, "Keccak_python.bits2bytes(15) should return 0.875")



# def random_state_generator():
#   state_matrix = []
#   for x in range(5):
#     row = []
#     for y in range(5):
#       random_int = secrets.randbits(64) # generates a random 64-bit int - for each lane
#       row.append(random_int)  
#     state_matrix.append(row) 
#   return state_matrix 



# # Generates an array 'states' which stores 3 random state arrays for testing
# def random_state_generator(num=3):
#   states = []
#   for i in range(num):
#     state_matrix = []
#     for x in range(5):
#       row = []
#       for y in range(5):
#         random_int = secrets.randbits(64) # generates a random 64-bit int - for each lane
#         row.append(random_int)  
#       state_matrix.append(row) 
#     states.append(state_matrix) 
#   return states

# # Convert python 2d list to C compatible format
# def convert_to_c_state(state):
#   # Define array type using ctypes lib 
#   c_row = c_uint64 * 5    # single row of 5 64-bit unsigned ints using ctypes 'c_uint64'     
#   # Instantiate the 5*5 matrix using c_row 
#   c_state = (c_row * 5)() #all elements are set to zero

#   # Populate c_state with python state values
#   for x in range(5):
#     for y in range(5):
#       c_state[x][y] = state[x][y]
  
#   return c_state          # returned state is now compatible with the keccak C functions
