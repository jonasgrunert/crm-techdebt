# Summary of Wikipedia

## Introduction

- "Implied cost of additional rework, [...] by choosing an easy (limited) solution [...] instead of using a better approach, that would take longer"
- "it can accumulate 'interest', makcing it harder to implement changes"
- "Unadressed [it][...] increases software entropy"
- It is not necessiarly bad, but the term might as well minimize the impact
- Uncompleted changes may also lead to tech debt

## Causes

- Insufficient definitions
- Business pressure
- Lack of technical undestanding on the business side
- Tightly coupled components
- Lack of tests, documentation, standards alignment, knowledge, ownership and/or collaboration
- Parallel development for a long time
- Delayed refactoring
- Last minute specification changes
- Poor technical leadership
- Code smells

## Types

See Martin Fowler
||Reckless| Prudent|
|--|--|--|
|Deliberate| No time | Deal later |
|Inadvertent| What | Now we know|

## Repayment

- Unaware of debt
- Known of debt
- Targeted for removal debt

## Consequences

- Missing the deadline based on unfinished or underestimated work
- Risk of outages due to refactoring
- Cost of new feature rises exponentially

# Notes to take with

- Software entropy is linked to tech debt
- Tech debt can occur outside of code
- Tech debts reasons are often outside of code
- Code smell can be an indicator for tech debt
