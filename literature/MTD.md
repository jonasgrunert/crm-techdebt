# Summary of an empirical model of technical debt

## Introduction

The paper defines technical debt as the cost to impove technical quality up to an ideal level. To qunatify technical debt they answer three questions:

- How large is my technical debt?
- How much interest am I payinng on the debt?
- Is the debt growing?

## Measuring technical debt

### Software Maintanibilty

Using a system based off IS/IEC 9126, which consists of multiple classical software quality metrics. They will betransalted into unitless ratings either based on ratio in LoC or make use of Risk Profile, which are based upon LoC Percentage threshholds.  
Building a dependcy tree of different metrics, which combine into one metric for the SIG quality model. Those are then again overall averaged into one metric.

### Quantifying technical debt

The Repait Effort is combined from two different metrics: Rework Fraction, whihc is an estimated percentage lines of code, that have to change. Rebuild Value is an estimate of the effort to rebuild a system using a particular technology.

### Quantifying the interest

Quantifying the interest takes in the Maintance Fraction needed with the Rebuild Value in contrast to the Quality factor. Maintenace Fraction and Quality Factor are highly coupled with the determined unitless level of the source code.

# Notes to take with

Based on code metrics it is easy to sort a piece of source code into a category of quality, for a status quo.
