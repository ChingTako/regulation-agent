def match(text):

    keywords = [
        "bike",
        "ebike",
        "medical device",
        "wheelchair"
    ]

    text = text.lower()

    return any(k in text for k in keywords)