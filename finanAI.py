import pandas as pd
import random
import re

class FinancialAssistant:
    def __init__(self, data):
        self.data = data
        self.shown_tips = []  # To track displayed tips

    def get_total_income_expense_savings(self):
        total_income = self.data[self.data['Type'] == 'Income']['Amount'].sum()
        total_expense = self.data[self.data['Type'] == 'Expense']['Amount'].sum()
        savings = total_income - total_expense
        return total_income, total_expense, savings

    def process_savings_query(self, query):
        savings_keywords = ['save', 'spend less', 'cut down', 'budget', 'saving tips', 'money tips', 'give me tips', 'give me saving tips', 'tell me saving tips', 'how to save']
        tips = [
            "1. Set a strict budget and stick to it.",
            "2. Track all your spending to identify areas of overspending.",
            "3. Consider reducing your luxury or non-essential expenses.",
            "4. Shop smarter: use coupons, discounts, and buy in bulk where possible.",
            "5. Put your savings in a high-interest account or investment for growth.",
            "6. Automate your savings to save a percentage of your income without thinking about it."
        ]

        if any(keyword in query.lower() for keyword in savings_keywords):
            print("\nHere are some personalized tips to save more money:\n")
            while True:
                # Randomly choose a tip that hasn't been shown yet
                available_tips = [tip for tip in tips if tip not in self.shown_tips]
                
                if not available_tips:  # If all tips have been shown, end the loop
                    print("\nYou have already seen all available saving tips!")
                    break

                # Select a new tip
                new_tip = random.choice(available_tips)
                print(new_tip)
                self.shown_tips.append(new_tip)  # Add the shown tip to the list

                user_response = input("\nWould you like another saving tip? (yes/no/skip): ").lower()
                if user_response in ['yes', 'y']:
                    continue
                elif user_response in ['no', 'n']:
                    print("Great! Feel free to ask for more tips anytime.")
                    break
                elif user_response == 'skip':
                    print("No problem! Feel free to ask about anything else.")
                    break
                else:
                    print("Sorry, I didn't understand that. Please respond with 'yes', 'no', or 'skip'.")
        else:
            print("It seems you're not asking specifically for saving tips. Please rephrase your question and try again.\n")

    def provide_expense_insights(self):
        expense_category = self.data[self.data['Type'] == 'Expense'].groupby('Category')['Amount'].sum()
        high_expenses = expense_category[expense_category > expense_category.mean()]
        if not high_expenses.empty:
            print("\nYou're overspending in these categories compared to your average monthly expenses:")
            print(high_expenses)
        else:
            print("\nYou're doing well! No overspending detected in your expense categories.")

    def offer_budget_reminder(self):
        user_response = input("Would you like a reminder to stick to your budget? (yes/no): ").lower()
        if user_response in ['yes', 'y']:
            print("\nHere's a reminder: Stick to your budget! Review your expenses regularly to avoid overspending.")
        else:
            print("Okay! Let me know if you need any reminders later.")

    def handle_query(self, query):
        if re.search(r'(income|total income)', query, re.I):
            total_income, _, _ = self.get_total_income_expense_savings()
            print(f"Your total income is: ${total_income:.2f}")

        elif re.search(r'(expenses?|spending)', query, re.I):
            _, total_expense, _ = self.get_total_income_expense_savings()
            print(f"Your total expenses are: ${total_expense:.2f}")

        elif re.search(r'(savings?|save)', query, re.I):
            _, _, savings = self.get_total_income_expense_savings()
            print(f"Your total savings are: ${savings:.2f}")

        elif re.search(r'(category expenses?|spending by category)', query, re.I):
            print("\nSpending breakdown by category:")
            expense_category = self.data[self.data['Type'] == 'Expense'].groupby('Category')['Amount'].sum()
            print(expense_category)

        elif re.search(r'(give me tips|how to save)', query, re.I):
            self.process_savings_query(query)

        elif re.search(r'(budget|reminder)', query, re.I):
            self.offer_budget_reminder()

        elif re.search(r'(insights|spending insights)', query, re.I):
            self.provide_expense_insights()

        else:
            print("Sorry, I didn't quite get that. Can you rephrase your question or try another one?")

# Simulate some financial data
data = {
    'Date': ['12/30/2023', '12/30/2023', '12/30/2023', '12/30/2023', '12/29/2023'],
    'Category': ['Tax', 'Supermarket', 'Monthly Rent', 'Tea', 'Freelancing'],
    'Type': ['Expense', 'Expense', 'Expense', 'Expense', 'Income'],
    'Amount': [39.16, 68.95, 1774.61, 49.02, 528.79]
}

df = pd.DataFrame(data)

# Instantiate the FinancialAssistant class
assistant = FinancialAssistant(df)

def main():
    print("Welcome to your AI Financial Assistant!")
    while True:
        print("\nMain Menu: Please choose an option:")
        print("1. Ask about total income")
        print("2. Ask about total expenses")
        print("3. Ask about savings")
        print("4. Ask about expenses by category")
        print("5. Get saving tips")
        print("6. Get expense insights")
        print("7. AI Assistant - Ask me anything")
        print("8. Exit")
        
        choice = input("Enter your choice (1-8): ")

        if choice == '1':
            assistant.handle_query("total income")
        elif choice == '2':
            assistant.handle_query("total expenses")
        elif choice == '3':
            assistant.handle_query("savings")
        elif choice == '4':
            assistant.handle_query("spending by category")
        elif choice == '5':
            assistant.handle_query("give me saving tips")
        elif choice == '6':
            assistant.handle_query("spending insights")
        elif choice == '7':
            print("\nHello! I'm your financial assistant. How can I help you today?")
            user_query = input("You can ask me anything about your finances (or type 'exit' to quit): ")
            if user_query.lower() == 'exit':
                break
            else:
                assistant.handle_query(user_query)
        elif choice == '8':
            print("Thank you for using the Financial Assistant. Goodbye!")
            break
        else:
            print("Invalid choice. Please choose a number between 1 and 8.")

if __name__ == "__main__":
    main()
