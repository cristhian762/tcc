import json


def main():
    with open("sambanova_results.json", "r", encoding="utf-8") as file:
        models = json.load(file)

    data = []

    for model in models:
        for resume in models[model]:
            for result in models[model][resume]:
                if result == "limit tokens":
                    continue

                if result == "json invalid":
                    continue

                if len(result) != 5:
                    data.append(resume)

    print(data)


if __name__ == "__main__":
    main()
