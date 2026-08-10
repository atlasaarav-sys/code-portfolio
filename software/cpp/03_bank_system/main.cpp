#include <iostream>
#include <memory>

#include "account.hpp"
#include "bank.hpp"

int main() {
    Bank bank;
    bank.add_account(std::make_unique<SavingsAccount>("S001", "Aarav", 1000.0, 0.02));
    bank.add_account(std::make_unique<CheckingAccount>("C001", "Sam", 500.0, 200.0));

    std::cout << "-- initial state --\n";
    bank.print_all();

    bank.transfer("S001", "C001", 250.0);
    std::cout << "\n-- after transferring 250 from S001 to C001 --\n";
    bank.print_all();

    if (auto *savings = dynamic_cast<SavingsAccount *>(bank.find_account("S001"))) {
        savings->apply_interest();
    }
    std::cout << "\n-- after applying interest to S001 --\n";
    bank.print_all();

    try {
        bank.find_account("C001")->withdraw(1000.0); // exceeds balance + overdraft
    } catch (const InsufficientFundsError &e) {
        std::cout << "\ncaught expected exception: " << e.what() << "\n";
    }

    bank.save_to_file("accounts.txt");
    std::cout << "\nSaved account snapshot to accounts.txt\n";

    return 0;
}
