# opens the command prompt and executes multiples commands
import os
from concurrent.futures import ThreadPoolExecutor
from rich.console import Console
from tqdm import tqdm
from datetime import datetime, timedelta
import sys 

INTERVAL_SIZE=20
# Define the number of threads to use
num_threads = 8


def split_time_range(start_date, end_date, interval_size):
        intervals = []
        from datetime import datetime
        current_start = datetime.strptime(start_date, "%Y-%m-%d")

        
        while current_start < datetime.strptime(end_date, "%Y-%m-%d"):
            current_end = min(current_start + interval_size, datetime.strptime(end_date, "%Y-%m-%d"))
            intervals.append((current_start, current_end))
            current_start = current_end
        
        return intervals

def process_time_interval(start, end):
     
    commandlist=[
        r"C:\src\assetflow\.venv\Scripts\activate.bat",
        r"cd C:\src\assetflow\src\ingestion",
        f"python assetflow_gnosis_pipeline_incremental.py {start.strftime('%Y-%m-%d')} {end.strftime('%Y-%m-%d')}"
    ]
  
    # execute the first pipeline
    console.print(f"Executing pipeline assetflow_gnosis_pipeline_incremental {start} {end}...", style="bold green")
    os.system(" & ".join(commandlist))
    console.print(f"Pipeline assetflow_gnosis_pipeline_incremental execution {start} {end} completed!", style="bold green")

def execute_in_threads(start_date, end_date, interval_size, num_threads):
    intervals = split_time_range(start_date, end_date, interval_size)
    
    
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Submit each interval to a separate thread
        futures = [executor.submit(process_time_interval, interval[0], interval[1]) for interval in intervals]
        
        # Optionally: wait for all threads to complete
        for future in futures:
            future.result()



console = Console()

if __name__ == '__main__':
    
    #calculate todays date
    import datetime
    #today = datetime.date.today()
    #yesterday = today - datetime.timedelta(days=1)
    #yesterday=yesterday.strftime('%Y-%m-%d')
    #convert to string format
    #today = today.strftime('%Y-%m-%d')

    # Define the size of each interval (e.g., 1 day intervals)
    interval_size = timedelta(days=INTERVAL_SIZE)
    startdate=sys.argv[1]
    enddate=sys.argv[2]
           
  
    
    # Execute the function in threads
    execute_in_threads(startdate, enddate, interval_size, num_threads)
   

    # execute the second pipeline
    commandlist=[
        r"C:\src\assetflow\.venv\Scripts\activate.bat",
        r"cd C:\src\assetflow\src\ingestion",
        f"python assetflow_gnosis_pipeline.py"
    ]
    console.print("Executing pipeline assetflow_gnosis_pipeline...", style="bold green")
    os.system(" & ".join(commandlist))
    console.print("Pipeline assetflow_gnosis_pipeline execution completed!", style="bold green")

   





