# Project 04: Employee Payroll Batch Processor

## Estimated Time
5 to 7 hours

## Goal
Create a payroll batch program that calculates monthly salaries.

## Functional Requirements
- Load employee data (base salary, allowances, deductions).
- Compute net pay per employee.
- Handle tax slab calculation.
- Generate payroll summary report:
  - total payroll amount
  - top 5 salaries
  - department-wise totals
- Export payroll output CSV.

## Non-Functional Requirements
- Invalid numeric values should be rejected.
- Keep per-employee error log for failed rows.

## Concepts Practiced
- `List<Map<String, String>>` input rows
- `Map<String, Double>` department totals
- sorting by net pay

## HLD
- `PayrollLoader`
- `PayrollCalculator`
- `PayrollReportService`
- `CsvExporter`

## LLD
- `loadEmployees(path): List<EmployeeRecord>`
- `calculateTax(gross): double`
- `calculateNet(employee): PayrollRecord`
- `departmentTotals(payrollList): Map<String, Double>`
- `topSalaries(payrollList, n): List<PayrollRecord>`
- `writePayrollCsv(path, payrollList): void`

## Passing Criteria
- Net pay formula correct.
- Department totals correct.
- CSV output created successfully.

## Implementation Roadmap
1. Build CSV loader.
2. Add payroll calculations.
3. Add report metrics.
4. Add export and validation checks.
