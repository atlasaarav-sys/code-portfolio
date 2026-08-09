#pragma once

#include <map>
#include <memory>
#include <string>

#include "account.hpp"

class Bank {
public:
    Account *add_account(std::unique_ptr<Account> account);
    Account *find_account(const std::string &id);

    void transfer(const std::string &from_id, const std::string &to_id, double amount);

    void save_to_file(const std::string &path) const;
    void print_all() const;

private:
    std::map<std::string, std::unique_ptr<Account>> accounts_;
};
