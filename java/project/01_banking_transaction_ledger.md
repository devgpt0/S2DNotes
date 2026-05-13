# Project 01: Banking Transaction Ledger

## Estimated Time
4 to 6 hours

## Goal
Build a core banking ledger module that records debit/credit transactions and generates account statements.

## Functional Requirements
- Create account with account number and holder name.
- Credit/debit amount.
- Block debit if balance is insufficient.
- Keep transaction history per account.
- Generate mini statement (last N transactions).
- Save/load data from file.

## Non-Functional Requirements
- Transaction ID must be unique.
- Amount must be positive.

## Concepts Practiced
- `Map<String, AccountRecord>` for account lookup
- `List<TransactionRecord>` per account
- `Collections.sort` for statement ordering

## HLD
- `AccountService`
- `TransactionService`
- `StatementService`
- `StorageService`

## LLD
- `createAccount(accounts, holder): AccountRecord`
- `credit(accounts, accountNo, amount): boolean`
- `debit(accounts, accountNo, amount): boolean`
- `getStatement(accounts, accountNo, n): List<TransactionRecord>`
- `saveData(path, accounts): void`
- `loadData(path): Map<String, AccountRecord>`

## Passing Criteria
- Debit over balance fails.
- Balance updates correctly after each transaction.
- Statement returns correct latest entries.

## Implementation Roadmap
1. Build account and transaction structures.
2. Implement credit/debit logic.
3. Add statement generation.
4. Add persistence and CLI menu.
