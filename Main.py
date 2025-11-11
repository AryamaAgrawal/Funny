#!/usr/bin/env python3
"""
FinBot 💬 - Copilot-Assisted Finance Chat (offline)

Development note (for your mentor):
# Copilot: Generate a dictionary of short, friendly finance explanations for common terms
# (e.g. "mutual fund", "compound interest", "inflation", "fixed deposit", "credit score").
# Provide 1-2 sentence plain-language answers suitable for demo.

The lines above are the Copilot prompt I used while developing this file.
At runtime the script uses these saved templates and runs fully offline.
"""

import random
import textwrap
import time
from datetime import datetime

# ----------------------
# Copilot-authored knowledge (static templates)
# ----------------------
FINANCE_KNOWLEDGE = {
    "mutual fund": "A mutual fund pools money from many investors and invests it in a diversified set of assets managed by professionals.",
    "compound interest": "Compound interest is interest on both the original amount and on previously earned interest — it makes savings grow faster over time.",
    "inflation": "Inflation is the general rise in prices over time, which reduces the purchasing power of money.",
    "fixed deposit": "A fixed deposit (FD) locks money for a fixed period at a set interest rate, offering stable returns with low risk.",
    "credit score": "A credit score is a number that shows how trustworthy you are with borrowed money — higher scores make it easier to get loans at better rates.",
    "loan": "A loan is borrowed money you must repay with interest over an agreed schedule; terms depend on the lender and your creditworthiness.",
    "savings account": "A savings account stores your money securely and pays small interest; it's useful for short-term goals and emergency funds.",
    "budgeting": "Budgeting means planning your income and expenses so you can save and avoid overspending.",
    "stock market": "The stock market is where investors buy and sell shares of companies — it can offer growth but comes with risk.",
    "tax": "Tax is a mandatory payment to the government used to fund public services like roads, healthcare, and education.",
    "emi": "EMI (Equated Monthly Installment) is the fixed monthly payment you make to repay a loan over its tenure.",
    "interest rate": "Interest rate is the percentage charged by lenders on borrowed money or paid by banks on deposits."
}

# Conversational flourishes Copilot could have suggested
OPENERS = [
    "That’s a great question! Here's a quick explanation:",
    "Good question — in simple terms:",
    "Here’s a quick breakdown:"
]

CLOSERS = [
    "Anything else you'd like to ask?",
    "Ask me another finance term or type 'exit' to quit.",
    "Type another question or 'exit' when you're done."
]

GOODBYES = [
    "Goodbye! Keep learning and save smartly 💰",
    "Bye — keep your finances healthy! 📈",
    "See you! Stay financially curious."
]

# Optional: small typing effect for demo polish (keeps it offline)
def type_print(text, delay=0.006):
    """Prints text with a small delay per character to mimic typing."""
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()

def answer_question(query: str) -> str:
    q = query.lower().strip()
    # exact-key matching first
    for key in FINANCE_KNOWLEDGE:
        if key in q:
            opener = random.choice(OPENERS)
            body = FINANCE_KNOWLEDGE[key]
            return f"{opener}\n\n{body}"
    # fallback guidance responses (Copilot could generate these)
    if "how" in q and "save" in q or "saving" in q:
        return "Try the 50/30/20 rule: 50% needs, 30% wants, 20% savings/investments."
    if "how" in q and ("invest" in q or "investment" in q):
        return "Start with low-cost index funds or an emergency fund first; diversify and invest for the long term."
    # generic fallback
    return ("I don't have a direct answer for that term yet. "
            "Try asking about: mutual fund, compound interest, inflation, credit score, or loan.")

def main():
    print("\nWelcome to FinBot 💬 (Copilot-assisted Finance Chat)\n")
    print("Ask me anything about finance, banking, or savings.")
    print("Type 'exit' to quit.\n")
    try:
        while True:
            user_input = input("> ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit", "bye"):
                print()
                type_print(random.choice(GOODBYES), delay=0.003)
                break
            # show timestamp for polish
            ts = datetime.now().strftime("%H:%M:%S")
            print(f"\n[FinBot • {ts}]")
            reply = answer_question(user_input)
            # pretty print reply
            for paragraph in reply.split("\n\n"):
                type_print(textwrap.fill(paragraph, width=78))
                print()
            # show closer line
            type_print(random.choice(CLOSERS))
            print()
    except (KeyboardInterrupt, EOFError):
        print()
        type_print(random.choice(GOODBYES), delay=0.003)


if __name__ == "__main__":
    main()
