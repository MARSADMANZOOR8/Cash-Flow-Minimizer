from flask import Flask, render_template, request, jsonify

class CashFlowMinimizer:
    def __init__(self, num_people):
        self.num_people = num_people
        self.net_balance = [0] * num_people

    def add_transaction(self, payer, payee, amount):
        """Record a transaction where `payer` owes `amount` to `payee`."""
        self.net_balance[payer] -= amount
        self.net_balance[payee] += amount

    def minimize_cash_flow(self):
        """Minimize the number of cash flow transactions."""
        def get_max_credit():
            return max(range(self.num_people), key=lambda x: self.net_balance[x])

        def get_max_debit():
            return min(range(self.num_people), key=lambda x: self.net_balance[x])

        def settle_debt(debtor, creditor):
            amount = min(-self.net_balance[debtor], self.net_balance[creditor])
            self.net_balance[debtor] += amount
            self.net_balance[creditor] -= amount
            transactions.append(f"Person {debtor} pays {amount} to Person {creditor}")

        transactions = []

        while True:
            debtor = get_max_debit()
            creditor = get_max_credit()

            if self.net_balance[debtor] == 0 and self.net_balance[creditor] == 0:
                break

            settle_debt(debtor, creditor)

        return transactions

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/minimize', methods=['POST'])
def minimize_cash_flow():
    data = request.json
    num_people = data['num_people']
    transactions = data['transactions']

    minimizer = CashFlowMinimizer(num_people)

    for transaction in transactions:
        payer, payee, amount = transaction
        minimizer.add_transaction(payer, payee, amount)

    optimized_transactions = minimizer.minimize_cash_flow()

    return jsonify({
        "transactions": optimized_transactions,
        "net_balance": minimizer.net_balance
    })

if __name__ == "__main__":
    app.run(debug=True)
