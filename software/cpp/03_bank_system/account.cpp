#include "account.hpp"

Account::Account(std::string id, std::string owner, double balance)
    : id_(std::move(id)), owner_(std::move(owner)), balance_(balance) {}

void Account::deposit(double amount) {
    if (amount <= 0) {
        throw std::invalid_argument("deposit amount must be positive");
    }
    balance_ += amount;
}

void Account::withdraw(double amount) {
    if (amount <= 0) {
        throw std::invalid_argument("withdrawal amount must be positive");
    }
    if (amount > balance_) {
        throw InsufficientFundsError("insufficient funds for withdrawal");
    }
    balance_ -= amount;
}

SavingsAccount::SavingsAccount(std::string id, std::string owner, double balance, double interest_rate)
    : Account(std::move(id), std::move(owner), balance), interest_rate_(interest_rate) {}

void SavingsAccount::apply_interest() {
    balance_ += balance_ * interest_rate_;
}

CheckingAccount::CheckingAccount(std::string id, std::string owner, double balance, double overdraft_limit)
    : Account(std::move(id), std::move(owner), balance), overdraft_limit_(overdraft_limit) {}

void CheckingAccount::withdraw(double amount) {
    if (amount <= 0) {
        throw std::invalid_argument("withdrawal amount must be positive");
    }
    if (amount > balance_ + overdraft_limit_) {
        throw InsufficientFundsError("withdrawal exceeds balance and overdraft limit");
    }
    balance_ -= amount;
}
