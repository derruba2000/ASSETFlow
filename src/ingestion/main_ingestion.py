# opens the command prompt and executes multiples commands
import os
from rich.console import Console


console = Console()

if __name__ == '__main__':
    
    #calculate todays date
    import datetime
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    yesterday=yesterday.strftime('%Y-%m-%d')
    #convert to string format
    today = today.strftime('%Y-%m-%d')

    commandlist=[
        r"C:\src\assetflow\.venv\Scripts\activate.bat",
        r"cd C:\src\assetflow\src\ingestion",
        f"python assetflow_gnosis_pipeline.py {yesterday} {today}"
    ]

  

    # execute the command
    console.print("Executing pipeline...", style="bold green")
    os.system(" & ".join(commandlist))
    console.print("Pipeline completed!", style="bold green")

