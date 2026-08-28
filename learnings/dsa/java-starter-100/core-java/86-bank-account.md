# 86. Encapsulate a Bank Account

**What you learn:** Java core java APIs and problem solving.

## Problem

Create an account whose balance changes only through deposit and withdraw.

## Example

~~~text
Input: deposit 100, withdraw 30
Output: balance = 70
~~~

## Simple idea

Keep state private and reject negative deposits or overdrafts.

## Java solution

~~~java
static final class BankAccount {
    private int balance;
    void deposit(int amount) { if (amount < 0) throw new IllegalArgumentException(); balance += amount; }
    boolean withdraw(int amount) { if (amount < 0 || amount > balance) return false; balance -= amount; return true; }
    int balance() { return balance; }
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

