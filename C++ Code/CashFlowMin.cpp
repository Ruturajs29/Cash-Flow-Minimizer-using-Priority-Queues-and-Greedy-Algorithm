#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include <queue>
#include <bits/stdc++.h>
struct Person
{
    char name[50];
    int netAmount;
};
// Global variable for net amounts
struct Person *listOfNetAmounts;

// Comparator for priority queues
struct compare
{
    bool operator()(const int &a, const int &b) const
    {
        return listOfNetAmounts[a].netAmount > listOfNetAmounts[b].netAmount; // Min heap for creditors
    }
};

int **graph;

void printAns(int **ansGraph, int numPeople, struct Person input[])
{
    printf("\nThe transactions for minimum cash flow are as follows:\n");
    for (int i = 0; i < numPeople; i++)
    {
        for (int j = 0; j < numPeople; j++)
        {
            if (ansGraph[i][j] != 0)
            {
                printf("%s pays Rs %d to %s\n", input[i].name, ansGraph[i][j], input[j].name);
            }
        }
    }
}

void minimizeCashFlow(int numPeople, struct Person input[], int numTransactions)
{
    listOfNetAmounts = (struct Person *)malloc(numPeople * sizeof(struct Person));

    // Calculate net amounts and populate priority queues
    std::priority_queue<int, std::vector<int>, compare> minHeap; // Min heap for debtors
    std::priority_queue<int> maxHeap;                            // Max heap for creditors

    for (int p = 0; p < numPeople; p++)
    {
        strcpy(listOfNetAmounts[p].name, input[p].name);
        int amount = 0;

        for (int i = 0; i < numPeople; i++)
        {
            amount += graph[i][p]; // Credit
            amount -= graph[p][i]; // Debit
        }

        listOfNetAmounts[p].netAmount = amount;

        if (listOfNetAmounts[p].netAmount < 0)
        {
            minHeap.push(p); // Debtor index 
        }
        else if (listOfNetAmounts[p].netAmount > 0)
        {
            maxHeap.push(p); // Creditor index
        }
    }
    // Initialize ansGraph
    int **ansGraph = (int **)malloc(numPeople * sizeof(int *));
    for (int i = 0; i < numPeople; i++)
    {
        ansGraph[i] = (int *)calloc(numPeople, sizeof(int)); // Initialize with zeros
    }

    // Greedy logic using priority queues
    while (!minHeap.empty() && !maxHeap.empty())
    {
        int minIndex = minHeap.top();
        int maxIndex = maxHeap.top();

        // Determine transaction amount
        int transactionAmount = abs(listOfNetAmounts[minIndex].netAmount) < listOfNetAmounts[maxIndex].netAmount
                                    ? abs(listOfNetAmounts[minIndex].netAmount)
                                    : listOfNetAmounts[maxIndex].netAmount;

        // Update amounts
        listOfNetAmounts[minIndex].netAmount += transactionAmount;
        listOfNetAmounts[maxIndex].netAmount -= transactionAmount;

        // Record transaction in ansGraph
        ansGraph[minIndex][maxIndex] += transactionAmount;

        // Update priority queues based on new net amounts
        if (listOfNetAmounts[minIndex].netAmount == 0)
        {
            minHeap.pop();
        }
        else
        {
            minHeap.push(minIndex);
        }

        if (listOfNetAmounts[maxIndex].netAmount == 0)
        {
            maxHeap.pop();
        }
        else
        {
            maxHeap.push(maxIndex);
        }
    }

    printAns(ansGraph, numPeople, input);

    // Free allocated memory
    for (int i = 0; i < numPeople; i++)
    {
        free(ansGraph[i]);
    }
    free(ansGraph);
}

int main()
{
    printf("\n\t\t\t\t********************* Welcome to CASH FLOW MINIMIZER ***********************\n\n");

    printf("Enter the number of people participating in the transactions: ");
    int numPeople;
    scanf("%d", &numPeople);

    struct Person *input = (struct Person *)malloc(numPeople * sizeof(struct Person)); // Creating structures

    printf("\nEnter the names of the people:\n");
    for (int i = 0; i < numPeople; i++)
    {
        printf("Person %d: ", i + 1);
        scanf("%s", input[i].name);
    }

    printf("\nEnter number of transactions: ");
    int numTransactions;
    scanf("%d", &numTransactions);

    graph = (int **)malloc(numPeople * sizeof(int *));
    for (int i = 0; i < numPeople; i++)
    {
        graph[i] = (int *)calloc(numPeople, sizeof(int)); // Initialize with zeros
    }
    for (int i = 0; i < numPeople; i++)
    {
        for (int j = 0; j < numPeople; j++)
        {
            std::cout << graph[i][j] << " ";
        }
        std::cout << "\n";
    }

    printf("Enter the details of each transaction as stated:\n");

    for (int i = 0; i < numTransactions; i++)
    {
        char debtor[50], creditor[50];
        int amount;

        printf("Transaction %d: ", i + 1);
        scanf("%s %s %d", debtor, creditor, &amount);

        for (int j = 0; j < numPeople; j++)
        {
            if (strcmp(input[j].name, debtor) == 0)
            {
                for (int k = 0; k < numPeople; k++)
                {
                    if (strcmp(input[k].name, creditor) == 0)
                    {
                        graph[j][k] += amount; // Store transaction in graph
                        break;
                    }
                }
                break;
            }
        }
    }

    minimizeCashFlow(numPeople, input, numTransactions);

    for (int i = 0; i < numPeople; i++)
    {
        free(graph[i]);
    }

    free(graph);
    free(input);

    return 0;
}