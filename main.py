import speedtest
import requests
import time
from datetime import datetime, timezone

ENDPOINT_URL = "https://tybodager-001-site9.gtempurl.com/Pioneer"
ACCOUNT_NAME = "Steven"
SENSOR_TYPE = "network"

def run_speedtest():
    print(f"[{datetime.now().strftime('%X')}] Initializing speedtest...")
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        st.download()
        st.upload()
        return st.results.dict()
    except Exception as e:
        print(f"[{datetime.now().strftime('%X')}] Speedtest failed: {e}")
        return None

def send_metric(data_key, data_value):
    payload = {
        "sensorType": SENSOR_TYPE,
        "dateTime": datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z'),
        "accountName": ACCOUNT_NAME,
        "dataKey": data_key,
        "dataValue": str(data_value)
    }
    
    try:
        response = requests.post(ENDPOINT_URL, json=payload)
        print(f"[{datetime.now().strftime('%X')}] Status: {response.status_code} | Sent {data_key}: {data_value}")
    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now().strftime('%X')}] Request failed for {data_key}: {e}")

def main():
    while True:
        results = run_speedtest()
        
        if results:
            # Extract metrics (converting bits to Megabits for down/up)
            download_mbps = round(results["download"] / 1_000_000, 2)
            upload_mbps = round(results["upload"] / 1_000_000, 2)
            ping_ms = round(results["ping"], 2)
            
            # Send each metric as a separate POST request
            send_metric("download_mbps", download_mbps)
            send_metric("upload_mbps", upload_mbps)
            send_metric("ping_ms", ping_ms)
        
        print(f"[{datetime.now().strftime('%X')}] Sleeping for 30 minutes...")
        time.sleep(1800) # 1800 seconds = 30 minutes

if __name__ == "__main__":
    main()