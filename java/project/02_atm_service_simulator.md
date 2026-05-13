# Project 02: ATM Service Simulator

## Estimated Time
4 to 6 hours

## Goal
Simulate ATM operations on top of banking accounts.

## Functional Requirements
- PIN-based login.
- Balance inquiry.
- Cash withdraw.
- Cash deposit.
- Transfer between accounts.
- Show last 5 ATM actions.

## Non-Functional Requirements
- Limit PIN retries (e.g., 3 attempts).
- Keep session log for each run.

## Concepts Practiced
- `Map<String, String>` for account->PIN
- `Map<String, Double>` balances
- `Deque<String>` for last actions

## HLD
- `AuthModule`
- `AtmOperations`
- `SessionLogger`
- `MainMenu`

## LLD
- `authenticate(accountNo, pin, pinStore): boolean`
- `withdraw(balanceMap, accountNo, amount): boolean`
- `deposit(balanceMap, accountNo, amount): boolean`
- `transfer(balanceMap, from, to, amount): boolean`
- `recordAction(actionsDeque, message): void`
- `getRecentActions(actionsDeque, n): List<String>`

## Passing Criteria
- Wrong PIN lock logic works.
- Withdraw/transfer validation works.
- Action history stores recent operations.

## Implementation Roadmap
1. Build auth flow.
2. Add ATM operations.
3. Add action history.
4. Add input handling and tests.
