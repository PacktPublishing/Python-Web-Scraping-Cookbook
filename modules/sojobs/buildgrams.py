def build_2grams(tokens, patterns):
    results = []
    left_token = None
    for i, t in enumerate(tokens):
        right_token = t
        if right_token.lower() == "web":
            pass
        if left_token is None:
            left_token = t
            continue



        if left_token.lower() in patterns:
            right = patterns[left_token.lower()]
            if right_token.lower() in right:
                results.append(left_token + right[right_token.lower()] + right_token)
                left_token = None
            else:
                results.append(left_token)
                left_token = right_token
        else:
            results.append(left_token)
            left_token = right_token

    if left_token is not None:
        results.append(left_token)
    return results

if __name__ == "__main__":
    grams = {
        'c': {'#': ''}
    }
    print(build_2grams(['C'], grams))
    print(build_2grams(['#'], grams))
    print(build_2grams(['C', '#'], grams))
    print(build_2grams(['c', '#'], grams))
