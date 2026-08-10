# 03 — Bank Account System

**Language:** C++17
**Level:** Advanced (for this track — first "real" application)

## What this demonstrates

- Multi-file project structure (headers + .cpp + build)
- Class design: encapsulation, `const` correctness, custom exceptions
- Inheritance (`SavingsAccount`, `CheckingAccount` extend `Account`)
- File persistence (simple CSV-style save/load)
- `std::map` for an account registry

## Files

- `account.hpp` / `account.cpp` — `Account` base class + derived account types
- `bank.hpp` / `bank.cpp` — `Bank` class managing a registry of accounts,
  handles deposits/withdrawals/transfers, save/load to `accounts.txt`
- `main.cpp` — demo program exercising the bank

## How to run

```bash
make
./bank_demo
```

## Notes

`accounts.txt` is created at runtime and gitignored — it's local demo state,
not source content.
