from sojobs.buildgrams import build_2grams

def tech_2grams(tokens):
    grams = {
        "c": {"#": ""},
        "sql": {"server": " "},
        "fast": {"paced": "-"},
        "highly": {"iterative": " "},
        "adapt": {"quickly": " "},
        "demonstrable": {"experience": " "},
        "full": {"stack": "-"},
        "enterprise": {"software": " "},
        "bachelor": {"s": "'"},
        "computer": {"science": " "},
        "data": {"science":  " "},
        "current": {"trends": " "},
        "real": {"world": "-"},
        "paid": {"relocation": " "},
        "web": {"server": " ", "development": " ", "technologies": " "},
        "relational": {"database": " "},
        "no": {"sql": " "},
        "client": {"side": "-"},
        "continuous": {
            "monitoring": " ",
            "integration": " ",
            "delivery": " "
        },
        "low": {"level": "-"},
        "information": {"technology": " "}
    }

    return build_2grams(tokens, grams)
