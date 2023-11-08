import threading
import requests
import time
from ConfigManager import ConfigManager

config = ConfigManager().getConfig()
responseTimes = []
threads = []


def generateGetRequest():
    headers = {"Connection": "keep-alive"}
    return requests.get(config["target_address"], headers=headers)


def client():
    while True:
        startTime = time.time()
        generateGetRequest()
        endTime = time.time()
        responseTime = endTime - startTime
        responseTimes.append(endTime - startTime)

        if responseTime > 60:
            print("O site parou de responder")
            break


def stressTester():
    for i in range(0, config["simultaneous_connections"]):
        thread = threading.Thread(target=client)
        threads.append(thread)
        thread.start()

    while any(thread.is_alive() for thread in threads):
        if len(responseTimes) == 0:
            continue

        averageResponseTime = sum(responseTimes) / len(responseTimes)
        print(f"Tempo de resposta médio da aplicação: {averageResponseTime:.2f}")


stressTester()
