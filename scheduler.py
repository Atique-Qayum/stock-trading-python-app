import scheduler
import time
from script import fetch_tickers

from datetime import datetime

def basic_job():
    print("Job started at " , datetime.now())
          
    scheduler.every().minute.do(basic_job)
                                
    scheduler.every().minute.do(fetch_tickers)
    while True:
        scheduler.run_pending()
        time.sleep(1)