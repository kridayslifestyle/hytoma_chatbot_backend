import time
import random


def typing_delay(message: str):

    words = len(message.split())

    # human typing speed
    base = words * 0.07

    # punctuation pause (very important)
    if "?" in message:
        base += 0.5
    if "!" in message:
        base += 0.3
    if "," in message:
        base += 0.2

    # randomness
    jitter = random.uniform(0.3, 1.2)

    delay = base + jitter

    delay = max(1.2, min(delay, 6))

    print(f"\n🟡 Human typing simulation: {delay:.2f}s")

    time.sleep(delay)