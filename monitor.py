from prometheus_client import start_http_server, Gauge
import requests, time

URLS = ["https://httpstat.us/503", "https://httpstat.us/200"]

up_metric = Gauge('sample_external_url_up', 'URL availability', ['url'])
response_time_metric = Gauge('sample_external_url_response_ms', 'Response time in ms', ['url'])

def check_url(url):
    try:
        start = time.time()
        response = requests.get(url, timeout=5)
        ms = (time.time() - start) * 1000
        up = 1 if response.status_code == 200 else 0
        up_metric.labels(url=url).set(up)
        response_time_metric.labels(url=url).set(ms)
        print(f"[✓] {url} — status: {response.status_code}, time: {ms:.2f} ms")
    except requests.RequestException as e:
        up_metric.labels(url=url).set(0)
        response_time_metric.labels(url=url).set(-1)
        print(f"[✗] {url} — error: {e}")

if __name__ == '__main__':
    print("Starting Prometheus metrics server on port 8000...")
    start_http_server(8000, addr="0.0.0.0")
    while True:
        for url in URLS:
            check_url(url)
        time.sleep(10)
