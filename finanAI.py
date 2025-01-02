import pandas as pd
import matplotlib.pyplot as plt
import spacy
import os
import random

file_path = "C:/Users/Dell/Downloads/transactions_converted.csv"

# Check if file exists
def check_file_exists():
    if os.path.exists(file_path):
        print("File found! Let's proceed.\n")
    else:
        print("Error: File not found! Exiting...\n")
        exit()

# Load Data and display basic info
def load_data():
    try:
        data = pd.read_csv(file_path)
        print("Data loaded successfully!")
        print(f"\nData preview:\n{data.head()}\n")
        return data
    except FileNotFoundError:
        print("Error: transactions_converted.csv not found! Exiting...\n")
        exit()

# Summarize by Category
def summarize_by_category(data):
    print("\nTotal Amount Spent by Category:")
    print(data.groupby('Category')['Amount'].sum(), "\n")

# Calculate and display income, expenses, and savings
def calculate_finances(data):
    total_income = data[data['Type'] == 'Income']['Amount'].sum()
    total_expense = data[data['Type'] == 'Expense']['Amount'].sum()
    savings = total_income - total_expense

    print(f"Total Income: ${total_income:.2f}")
    print(f"Total Expense: ${total_expense:.2f}")
    print(f"Savings: ${savings:.2f}\n")

# Visualize Spending by Category
def visualize_data(data):
    data.groupby('Category')['Amount'].sum().plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title("Amount Spent by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount ($)")
    plt.tight_layout()
    plt.show()

# Add User Input for New Expense
def add_new_expense(data):
    while True:
        try:
            category = input("Enter a new expense category (e.g., 'Food', 'Entertainment'): ").strip()
            amount = float(input("Enter the amount spent in this category: $"))
            data = pd.concat([data, pd.DataFrame([{'Category': category, 'Amount': amount, 'Type': 'Expense'}])], ignore_index=True)
            data.to_csv(file_path, index=False)
            print(f"New expense of ${amount:.2f} added to the '{category}' category!\n")
            break
        except ValueError:
            print("Invalid input. Please enter the amount as a numeric value.\n")
    return data

# NLP for Saving Suggestions
def process_savings_query(query):
    savings_keywords = ['save', 'spend less', 'cut down', 'budget', 'saving tips', 'money tips', 'give me tips', 'give me saving tips', 'tell me saving tips', 'how to save']
    tips = [
        "1. Set a strict budget and stick to it.",
        "2. Track all your spending to identify areas of overspending.",
        "3. Consider reducing your luxury or non-essential expenses.",
        "4. Shop smarter: use coupons, discounts, and buy in bulk where possible.",
        "5. Put your savings in a high-interest account or investment for growth.",
        "6. Automate your savings to save a percentage of your income without thinking about it."
    ]
    
    # Match any of the saving-related phrases
    if any(keyword in query.lower() for keyword in savings_keywords):
        shown_tips = []  # List to keep track of the tips shown
        
        print("\nHere are some personalized tips to save more money:\n")
        while True:
            # Randomly choose a tip that hasn't been shown yet
            available_tips = [tip for tip in tips if tip not in shown_tips]
            
            if not available_tips:  # If all tips have been shown, end the loop
                print("\nYou have already seen all available saving tips!")
                break
            
            # Select a new tip
            new_tip = random.choice(available_tips)
            print(new_tip)
            shown_tips.append(new_tip)  # Add the shown tip to the list

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

# NLP to understand Expense Queries
def process_expense_query(query, data):
    category = None
    doc = nlp(query)
    for token in doc:
        if token.pos_ in ['NOUN', 'PROPN']:
            category = token.text
            break
    
    if category:
        total_spent = data[data['Category'].str.contains(category, case=False, na=False)]['Amount'].sum()
        if total_spent > 0:
            print(f"\nTotal spent on {category}: ${total_spent:.2f}\n")
        else:
            print(f"No expenses found for the category '{category}'\n")
    else:
        print("Unable to process your query. Could you please rephrase your question?\n")

# AI Interaction Based on Natural Language
def ai_assistant():
    print("\nHello! I'm your financial assistant. How can I help you today?\n")
    while True:
        query = input("You can ask me anything about your finances (or type 'exit' to quit): ").strip().lower()

        if query == 'exit':
            print("\nGoodbye! Take care of your finances!")
            break
        elif 'tips' in query or 'save' in query:
            process_savings_query(query)
        elif 'spend' in query or 'how much' in query or 'amount' in query:
            process_expense_query(query, data)
        else:
            print("\nI'm not sure how to help with that. Can you ask me about your spending or saving tips?\n")

# Main Interaction Function
def main_interaction():
    global data
    nlp = spacy.load('en_core_web_sm')

    check_file_exists()
    data = load_data()
    
    while True:
        print("\nMain Menu: Please choose an option:")
        print("1. View total amount spent by category.")
        print("2. View your total income, expenses, and savings.")
        print("3. Visualize spending by category (Bar Chart).")
        print("4. Add a new expense.")
        print("5. Ask for saving tips.")
        print("6. Ask about specific expenses by category.")
        print("7. AI Assistant - Ask me anything (I respond in a conversational way).")
        print("8. Exit.")

        choice = input("\nEnter your choice (1-8): ").strip()

        if choice == "1":
            summarize_by_category(data)
        elif choice == "2":
            calculate_finances(data)
        elif choice == "3":
            visualize_data(data)
        elif choice == "4":
            data = add_new_expense(data)
        elif choice == "5":
            query = input("\nAsk for saving tips (e.g., 'Give me some tips to save money'): ").strip()
            process_savings_query(query)
        elif choice == "6":
            query = input("\nAsk a query about specific expenses (e.g., 'How much did I spend on food last month?'): ").strip()
            process_expense_query(query, data)
        elif choice == "7":
            ai_assistant()
        elif choice == "8":
            print("Thank you for using the Financial Tracker. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please select a valid option.\n")

# Run the main interaction loop
if __name__ == "__main__":
    main_interaction()
