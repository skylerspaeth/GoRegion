import time
for i in range(100):
    print("", end=f"\rPercentComplete: {i} %")
    time.sleep(0.2)
