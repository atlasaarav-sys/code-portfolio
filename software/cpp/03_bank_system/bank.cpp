#include "bank.hpp"

#include <fstream>
#include <iostream>
#include <stdexcept>

Account *Bank::add_account(std::unique_ptr<Account> account) {
    Account *ptr = account.get();
    accounts_[account->id()] = std::move(account);
    return ptr;
}

Account *Bank::find_account(const std::string &id) {
    auto it = accounts_.find(id);
    return it != accounts_.end() ? it->second.get() : nullptr;
}

void Bank::transfer(const std::string &from_id, const std::string &to_id, double amount) {
    Account *from = find_account(from_id);
    Account *to = find_account(to_id);
    if (!from || !to) {
        throw std::invalid_argument("unknown account id in transfer");
    }
    from->withdraw(amount);
    to->deposit(amount);
}

void Bank::save_to_file(const std::string &path) const {
    std::ofstream out(path);
    for (const auto &[id, account] : accounts_) {
        out << id << "," << account->owner() << "," << account->type() << "," << account->balance() << "\n";
    }
}

void Bank::print_all() const {
    for (const auto &[id, account] : accounts_) {
        std::cout << id << " (" << account->type() << ") owner=" << account->owner()
                  << " balance=" << account->balance() << "\n";
    }
}
