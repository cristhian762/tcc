import json


def sanitize(models):
    for model in models:
        for resume in models[model]:
            for result in models[model][resume]:
                if result == "limit tokens":
                    models[model][resume] = []
                    continue

                if result == "json invalid":
                    models[model][resume] = []
                    continue

                if len(models[model][resume]) > 5:
                    models[model][resume] = models[model][resume][0:5]

    return models


def accuracy(models):
    model_names = [
        "Meta-Llama-3.2-1B-Instruct",
        "Meta-Llama-3.1-8B-Instruct",
        "Meta-Llama-3.3-70B-Instruct",
        "Llama-4-Scout-17B-16E-Instruct",
    ]

    dic = {}

    for model_name in model_names:
        with open("separator_for_test.json", "r", encoding="utf-8") as file:
            test = json.load(file)

        accuracy = 0

        n_results_array = [1, 5]

        for n_results in n_results_array:
            accuracy = 0

            for name in test:
                with open(
                    "resumes/original/" + name + ".lab", "r", encoding="windows-1252"
                ) as file:
                    labels = file.read().replace("\n", ",").split(",")

                results = models[model_name][name][0:n_results]

                hits = 0

                for label in labels:
                    for item in results:
                        with open(
                            "resumes/original/" + item + ".lab",
                            "r",
                            encoding="windows-1252",
                        ) as file:
                            itemLabels = file.read().replace("\n", ",").split(",")

                        if label in itemLabels:
                            hits += 1

                accuracy += hits / len(labels)

            total_accuracy = accuracy / len(test) / n_results

            print(
                "Número de resultados {} Acurácia {}".format(n_results, total_accuracy)
            )

            if model_name not in dic.keys():
                dic[model_name] = {}

            dic[model_name][n_results] = total_accuracy

    with open("accuracy_llm.json", "w") as file:
        json.dump(dic, file, indent=2)


def main():
    with open("sambanova_results.json", "r", encoding="utf-8") as file:
        models = json.load(file)

    models = sanitize(models)
    accuracy(models)


if __name__ == "__main__":
    main()
