from django.shortcuts import render
from django.http import JsonResponse
from .models import Person, Transaction
from collections import defaultdict
import json

def index(request):
    return render(request, 'index.html')

def minimize_cash_flow(request):
    if request.method == 'GET':
        persons_data = json.loads(request.GET.get('persons', '[]'))
        transactions_data = json.loads(request.GET.get('transactions', '[]'))

        # Create Person instances
        persons = {name: Person.objects.get_or_create(name=name)[0] for name in persons_data}

        # Create Transaction instances
        transactions = []
        for trans in transactions_data:
            debtor = persons[trans['debtor']]
            creditor = persons[trans['creditor']]
            amount = trans['amount']
            transactions.append(Transaction(debtor=debtor, creditor=creditor, amount=amount))
        
        # Minimize cash flow
        minimized_transactions = minimize_cash_flow_logic(transactions)

        # Prepare graph data for visualization
        nodes = [{'data': {'id': name}} for name in persons_data]
        original_edges = [{'data': {'source': trans['debtor'], 'target': trans['creditor'], 'label': str(trans['amount'])}} for trans in transactions_data]
        minimized_edges = [{'data': {'source': t['debtor'], 'target': t['creditor'], 'label': str(t['amount'])}} for t in minimized_transactions]

        # Prepare response data
        response_data = {
            'minimized_transactions': minimized_transactions,
            'original_transactions': [{'debtor': t.debtor.name, 'creditor': t.creditor.name, 'amount': t.amount} for t in transactions],
            'graph_data': {
                'nodes': nodes,
                'original_edges': original_edges,
                'minimized_edges': minimized_edges,  # Ensure this data is passed correctly
            }
        }

        return render(request, 'cash_flow_minimizer.html', {'result': response_data})

def minimize_cash_flow_logic(transactions):
    # Calculate net amounts
    net_amounts = defaultdict(float)
    
    for transaction in transactions:
        net_amounts[transaction.debtor.name] -= transaction.amount
        net_amounts[transaction.creditor.name] += transaction.amount

    # Prepare lists for debtors and creditors
    debtors = [(name, amount) for name, amount in net_amounts.items() if amount < 0]
    creditors = [(name, amount) for name, amount in net_amounts.items() if amount > 0]

    minimized_transactions = []

    while debtors and creditors:
        debtor_name, debtor_amount = debtors.pop()
        creditor_name, creditor_amount = creditors.pop()

        transaction_amount = min(-debtor_amount, creditor_amount)

        minimized_transactions.append({
            'debtor': debtor_name,
            'creditor': creditor_name,
            'amount': transaction_amount,
        })

        # Update amounts
        if -debtor_amount > transaction_amount:
            debtors.append((debtor_name, debtor_amount + transaction_amount))
        
        if creditor_amount > transaction_amount:
            creditors.append((creditor_name, creditor_amount - transaction_amount))

    return minimized_transactions
