import time
import os
from database import init_script

if __name__ == '__main__':
    start_time = time.time()
    init_script(w_path=os.getcwd())
    print("--- %s seconds ---" % (time.time() - start_time))
