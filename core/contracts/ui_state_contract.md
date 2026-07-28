# RME UI State Contract v1.0

## Purpose

This document defines the official visual states used by the RME user interface.

UI states communicate operational information to the user.

They are independent from selection state.

---

## Design Principle

Selection is not Queue.

Queue is not Conversion.

Each concept must have its own visual language.

A checkbox must never imply that a file is currently being processed.

---

# Selection States

Selection only exists inside the Library Tree.

Selection determines what may be added to the queue.

Official selection states:

- Unselected
- Partially Selected
- Selected

Selection has no relationship with conversion status.

---

# Queue States

Queue states describe scheduling.

Official queue states:

- Not Queued
- Queued

Queued items are waiting for execution.

---

# Conversion States

Conversion states describe execution.

Official conversion states:

- Idle
- Running
- Completed
- Skipped
- Failed

Only one item may be Running at a time in v1.0.

---

# Visual Priority

Conversion State

>

Queue State

>

Selection State

Operational information always has higher priority than browsing information.

---

# State Ownership

Library Tree

- Selection State

Queue

- Queue State

ConversionService

- Conversion State

Each system owns only its corresponding state.

---

# Out of Scope

Planning

Analyzing

Validating

Verifying Output

ETA

Pause

Resume

Retry

These states require backend support and belong to future versions.