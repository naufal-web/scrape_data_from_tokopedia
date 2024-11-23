import csv

budget = 1400000
out_stock = 300
recommendations = set()

with open(r"C:\Users\62853\PycharmProjects\cashier_app\resources\brankas.csv") as csv_file:
    csv_reader = csv.reader(csv_file)
    csv_contents = list(csv_reader)[1:]


def normalize_data(example: list):
    sls = []
    for ls in example:
        temp = []
        for ele in ls:
            if ele.isdigit():
                temp.append(int(ele))
            else:
                temp.append(ele)
        sls.append(temp)
    return sls


for i in range(len(csv_contents)):
    for j in range(1, len(csv_contents)):
        for k in range(2, len(csv_contents)+1):
            if len(csv_contents[i:j:k]) == 2:
                comparing_data = csv_contents[i:j:k]
                comparing_data = normalize_data(comparing_data)
                if comparing_data[0][1] >= comparing_data[1][1] and comparing_data[1][2] >= out_stock:
                    price_remain = comparing_data[0][1] - comparing_data[1][1]
                    price_ratio = comparing_data[0][1] / comparing_data[1][1]
                    if comparing_data[1][1] < budget:
                        recommendations.add((comparing_data[1][0], comparing_data[1][1], comparing_data[1][2]))

                    if comparing_data[0][1] < budget and comparing_data[0][2] >= out_stock:
                        recommendations.add((comparing_data[0][0], comparing_data[0][1], comparing_data[0][2]))

                elif comparing_data[0][1] <= comparing_data[1][1] and comparing_data[0][2] >= out_stock:
                    price_remain = comparing_data[1][1] - comparing_data[0][1]
                    price_ratio = comparing_data[1][1] / comparing_data[0][1]
                    if comparing_data[0][1] < budget:
                        recommendations.add((comparing_data[0][0], comparing_data[0][1], comparing_data[0][2]))

                    if comparing_data[1][1] < budget and comparing_data[1][2] >= out_stock:
                        recommendations.add((comparing_data[1][0], comparing_data[1][1], comparing_data[1][2]))

for recommendation in recommendations:
    print(recommendation)
