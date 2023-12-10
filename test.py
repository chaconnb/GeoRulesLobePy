
import subprocess 

n_tests = 20
n_failed_test = 0 
for test in range(n_tests): 
    print(test)
    try:
        cmd = "python georules/M_LRBM.py".split() 
        subprocess.check_call(cmd)
        
    except: 
        n_failed_test += 1 


print(f"{n_failed_test=}")        