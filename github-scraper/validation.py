from statistics import mean, median
import requests
import json
import sys
import csv

annotation_api_url = 'http://localhost:8081/api/v1/highlight'
max_iterations = 3


def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def validate(code_lang):

    iteration = 1
    batch_size = 1500
    header = ['id', 'delay', 'correctPrediction']


    # Read json file
    with open(f'oracle-ds-{code_lang}.json', 'r') as f:
        json_data = f.read()

    oracle_ds = json.loads(json_data)

    oracle_ds_batches = list(divide_chunks(oracle_ds, batch_size))


    while (iteration <= max_iterations):

        counter = 1
        batch = oracle_ds_batches[iteration-1]

        with open(f'oracle-ds-{code_lang}-results-{iteration}', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(header)


            for el in batch:
                res = requests.post(annotation_api_url, json={
                "codeLanguage": code_lang,
                "sourceCode": el['sourceCode']
                })

                response_data = res.json()

                if response_data and response_data['prediction']:
                    #  Remove last item from hCodeValues since it is End-of-line token

                    formal = list(el['hCodeValues'])[:-1]
                    correct = set(response_data['prediction']) == set(formal)
                    row = [el['_id']['$oid'], round(res.elapsed.total_seconds() * 1000, 2), correct]
                    writer.writerow(row)
                else:
                    print("NO")
                    row = [el['_id']['$oid'], round(res.elapsed.total_seconds() * 1000, 2), False]
                    writer.writerow(row)
    
                print(f'File {counter} predicted')
                counter += 1
            f.close()

        overall_delays = []
        correct_predictions = 0

        with open(f'oracle-ds-{code_lang}-results-{iteration}', 'r') as responses_csv_file:
            csv_reader = csv.DictReader(responses_csv_file)

            for row in csv_reader:
                overall_delays.append(float(row['delay']))

                if row['correctPrediction'] == 'True':
                    correct_predictions += 1
            responses_csv_file.close()

        accuracy = correct_predictions / len(batch) * 100

        with open(f'result-{code_lang}-{iteration}.txt', 'w') as w:
            w.write(f"STATS FOR ITERATION {iteration}\n")
            w.write(f"BATCH SIZE {batch_size}\n")
            w.write(f'MAX DELAY: {max(overall_delays)}\n')
            w.write(f'AVG DELAY: {round(mean(overall_delays), 2)}\n')
            w.write(f'MEDIAN DELAY: { median(overall_delays)}\n')
            w.write(f'MIN DELAY: {min(overall_delays)}\n')
            w.write(f'ACCURACY: {accuracy}\n')
            w.close()

        input("Press any key to start next iteration")

        iteration += 1
    

if __name__ == '__main__':
    validate(sys.argv[1])


  