"""
Bank Token Queue System
DSC in Python - Mini Project

Data structures used:
  - deque  : FIFO queue for regular customers
  - heapq  : priority queue (min-heap) for senior citizens
Pure Python, runs in the terminal. No HTML / Flask needed.

Run:  python app.py
"""

import heapq
from collections import deque
from datetime import datetime


class BankTokenSystem:
    """Core DSA logic: deque (FIFO queue) + heapq (priority queue)."""

    def __init__(self):
        self.token_counter = 1
        self.normal_queue = deque()   # FIFO queue for regular customers
        self.priority_heap = []       # min-heap for senior citizens
        self.history = []             # served customers
        self.stats = {"Regular": 0, "Senior": 0}
        self.now_serving = None

    def issue_token(self, name, customer_type):
        token = self.token_counter
        self.token_counter += 1
        customer = {
            "token": f"T{token:03d}",
            "num": token,
            "name": name,
            "type": customer_type,
            "time": datetime.now().strftime("%H:%M:%S"),
        }
        if customer_type == "Senior":
            heapq.heappush(self.priority_heap, (token, customer))
        else:
            self.normal_queue.append(customer)
        self.stats[customer_type] += 1
        return customer

    def serve_next(self):
        # Senior citizens are always served first
        if self.priority_heap:
            _, customer = heapq.heappop(self.priority_heap)
        elif self.normal_queue:
            customer = self.normal_queue.popleft()
        else:
            return None
        self.history.append(customer)
        self.now_serving = customer
        return customer

    def waiting_count(self):
        return len(self.priority_heap) + len(self.normal_queue)

    def priority_list(self):
        return [c for _, c in sorted(self.priority_heap, key=lambda x: x[0])]

    def regular_list(self):
        return list(self.normal_queue)

    def reset(self):
        self.__init__()


# ---------------------------------------------------------------
# Terminal interface
# ---------------------------------------------------------------

LINE = "=" * 52


def show_status(bank):
    print("\n" + LINE)
    print("        BANK TOKEN QUEUE SYSTEM")
    print(LINE)
    print(f"Tokens issued : {bank.token_counter - 1}")
    print(f"Waiting       : {bank.waiting_count()}")
    print(f"Served        : {len(bank.history)}")
    print(f"Senior / Regular : {bank.stats['Senior']} / {bank.stats['Regular']}")
    if bank.now_serving:
        c = bank.now_serving
        print(f"NOW SERVING   : {c['token']} - {c['name']} ({c['type']})")
    else:
        print("NOW SERVING   : Nobody served yet")
    print(LINE)


def menu():
    print("1. Issue New Token")
    print("2. Serve Next Customer")
    print("3. Show Priority Queue (Senior Citizens)")
    print("4. Show Regular Queue (FIFO)")
    print("5. Show Served History")
    print("6. Reset for New Day")
    print("7. Exit")
    return input("Enter your choice (1-7): ").strip()


def issue(bank):
    name = input("Customer name: ").strip()
    if not name:
        print("Error: Customer name cannot be empty.")
        return
    print("Customer type:  1. Regular   2. Senior Citizen (Priority)")
    ctype = "Senior" if input("Choose (1/2): ").strip() == "2" else "Regular"
    c = bank.issue_token(name, ctype)
    print(f"Success: Token {c['token']} issued to {c['name']} ({c['type']}).")


def serve(bank):
    c = bank.serve_next()
    if c is None:
        print("Error: No customers waiting.")
    else:
        print(f"Success: Now serving {c['token']} - {c['name']} ({c['type']}).")


def show_queue(title, customers, empty_msg):
    print(f"\n--- {title} ---")
    if not customers:
        print(empty_msg)
        return
    for c in customers:
        print(f"{c['token']} - {c['name']:<15} (issued at {c['time']})")


def show_history(bank):
    print("\n--- Served History ---")
    if not bank.history:
        print("No customers served yet")
        return
    print(f"{'Token':<8}{'Name':<16}{'Type':<10}{'Issued at'}")
    for c in reversed(bank.history):
        print(f"{c['token']:<8}{c['name']:<16}{c['type']:<10}{c['time']}")


def main():
    bank = BankTokenSystem()
    while True:
        show_status(bank)
        choice = menu()
        if choice == "1":
            issue(bank)
        elif choice == "2":
            serve(bank)
        elif choice == "3":
            show_queue("Priority Queue (Senior Citizens)",
                       bank.priority_list(), "No senior citizens waiting")
        elif choice == "4":
            show_queue("Regular Queue (FIFO)",
                       bank.regular_list(), "No regular customers waiting")
        elif choice == "5":
            show_history(bank)
        elif choice == "6":
            if input("Reset everything? (y/n): ").strip().lower() == "y":
                bank.reset()
                print("Success: System reset for a new day.")
        elif choice == "7":
            print("Thank you! Goodbye.")
            break
        else:
            print("Invalid choice, please enter 1-7.")


if __name__ == "__main__":
    main()
