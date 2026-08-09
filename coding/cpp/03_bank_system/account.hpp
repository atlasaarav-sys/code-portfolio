#pragma once

#include <stdexcept>
#include <string>

class InsufficientFundsError : public std::runtime_error {
public:
    explicit InsufficientFundsError(const std::string &msg) : std::runtime_error(msg) {}
};

class Account {
public:
    Account(std::string id, std::string owner, double balance);
    virtual ~Account() = default;

    void deposit(double amount);
    virtual void withdraw(double amount); // savings/checking can differ (overdraft rules)

    const std::string &id() const { return id_; }
    const std::string &owner() const { return owner_; }
    double balance() const { return balance_; }

    virtual std::string type() const = 0;

protected:
    std::string id_;
    std::string owner_;
    double balance_;
};

class SavingsAccount : public Account {
public:
    SavingsAccount(std::string id, std::string owner, double balance, double interest_rate);

    void apply_interest();
    std::string type() const override { return "Savings"; }

private:
    double interest_rate_;
};

class CheckingAccount : public Account {
public:
    CheckingAccount(std::string id, std::string owner, double balance, double overdraft_limit);

    void withdraw(double amount) override;
    std::string type() const override { return "Checking"; }

private:
    double overdraft_limit_;
};
