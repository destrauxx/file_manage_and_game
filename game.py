def save():
    return {
        "level": 1,
        "obstacles": {
            "easy": 10,
            "medium": 15,
            "hard": 5,
        },
        "word": "orange"
}

def load(data):
    print(data)