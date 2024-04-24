import subprocess
import importlib.util
import multiprocessing

# Import your solver script
solver_spec = importlib.util.spec_from_file_location("solve", "solve.py")
solver_module = importlib.util.module_from_spec(solver_spec)
solver_spec.loader.exec_module(solver_module)

def one_gadget(filename):
    return [int(i) for i in subprocess.check_output(['one_gadget', '--raw', filename, "-l", "3"]).decode().split(' ')]

def test_solver_with_gadgets(solver_script, gadgets, output_file):
    def run_solver(gadget, result_queue):
        result_list = []
        try:
            # Call your solver script with the current gadget
            # Replace 'solve' with the actual function in your solver script
            result_iterator = solver_module.solve(gadget)
            for line in result_iterator:
                result_list.append(line)
        except Exception as e:
            result_list.append(f"Error occurred: {str(e)}")
        finally:
            result_queue.put(result_list)

    with open(output_file, 'w') as f:
        for gadget in gadgets[3:]:
            f.write(f"Testing solver with gadget: {hex(gadget)}\n")
            result_queue = multiprocessing.Queue()
            p = multiprocessing.Process(target=run_solver, args=(gadget, result_queue))
            p.start()
            p.join()
            result = result_queue.get()
            for line in result:
                f.write(f"Result: {line}\n")

# Get gadgets from libc.so.6
gadgets = one_gadget('libc.so.6')

# Define the output file
output_file = 'solver_test_results.txt'

# Test solver with each gadget and write results to file
test_solver_with_gadgets(solver_module, gadgets, output_file)
