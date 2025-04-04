import heapq

class Person:
    def __init__(self, name):
        self.name = name
        self.net_amount = 0

def print_ans(ans_graph, num_people, input_list):
    print("\nThe transactions for minimum cash flow are as follows:")
    for i in range(num_people):
        for j in range(num_people):
            if ans_graph[i][j] != 0:
                print(f"{input_list[i].name} pays Rs {ans_graph[i][j]} to {input_list[j].name}")

def minimize_cash_flow(num_people, input_list, graph):
    list_of_net_amounts = [Person(input_list[i].name) for i in range(num_people)]

    min_heap = []  # Min heap for debtors
    max_heap = []  # Max heap for creditors

    for p in range(num_people):
        amount = 0

        for i in range(num_people):
            amount += graph[i][p]  # Credit
            amount -= graph[p][i]  # Debit

        list_of_net_amounts[p].net_amount = amount

        if list_of_net_amounts[p].net_amount < 0:
            heapq.heappush(min_heap, (list_of_net_amounts[p].net_amount, p))  # Debtor
        elif list_of_net_amounts[p].net_amount > 0:
            heapq.heappush(max_heap, (-list_of_net_amounts[p].net_amount, p))  # Creditor (negative for max heap)

    # Initialize ans_graph
    ans_graph = [[0 for _ in range(num_people)] for _ in range(num_people)]

    # Transaction logic using heaps
    while min_heap and max_heap:
        min_amount, min_index = heapq.heappop(min_heap)
        max_amount, max_index = heapq.heappop(max_heap)

        transaction_amount = min(abs(min_amount), abs(max_amount))

        list_of_net_amounts[min_index].net_amount += transaction_amount
        list_of_net_amounts[max_index].net_amount -= transaction_amount

        ans_graph[min_index][max_index] += transaction_amount

        if list_of_net_amounts[min_index].net_amount < 0:
            heapq.heappush(min_heap, (list_of_net_amounts[min_index].net_amount, min_index))
        if list_of_net_amounts[max_index].net_amount > 0:
            heapq.heappush(max_heap, (-list_of_net_amounts[max_index].net_amount, max_index))

    print_ans(ans_graph, num_people, input_list)

def main():
    print("\n\t\t\t\t********************* Welcome to CASH FLOW MINIMIZER SYSTEM ***********************\n\n")
    
    num_people = int(input("Enter the number of people participating in the transactions: "))

    input_list = []
    print("\nEnter the names of the people:")
    for i in range(num_people):
        name = input(f"Person {i + 1}: ")
        input_list.append(Person(name))

    num_transactions = int(input("\nEnter number of transactions: "))

    graph = [[0 for _ in range(num_people)] for _ in range(num_people)]

    print("Enter the details of each transaction as stated:")

    for i in range(num_transactions):
        debtor, creditor, amount = input(f"Transaction {i + 1}: ").split()
        amount = int(amount)

        debtor_index = next(j for j, person in enumerate(input_list) if person.name == debtor)
        creditor_index = next(j for j, person in enumerate(input_list) if person.name == creditor)

        graph[debtor_index][creditor_index] += amount

    minimize_cash_flow(num_people, input_list, graph)

if __name__ == "__main__":
    main()
