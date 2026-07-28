# RME Visual Language v1.0

## Purpose

This document defines the official visual language used throughout the RME user interface.

The goal is consistency.

Every visual element must communicate a single meaning.

The same state must always be represented in the same way.

---

# Design Philosophy

The interface is an operational console.

Visual elements exist to communicate information quickly.

Decoration is secondary.

Clarity always has priority over aesthetics.

---

# Information Priority

Information should be presented in the following order of importance:

1. Current Conversion State
2. Queue Status
3. Batch Progress
4. Selected Item Information
5. Technical Metadata

The operator should never lose sight of what the engine is currently doing.

---

# Visual Communication Rules

One meaning per visual element.

Never reuse the same visual cue to represent different concepts.

Examples:

Checkboxes represent Selection.

Status Indicators represent Conversion State.

Progress Bars represent Progress.

Labels represent Information.

Icons reinforce meaning but never replace text.

---

# Selection Language

Selection communicates user intention.

Selection never communicates execution.

Official selection states:

- Unselected
- Partially Selected
- Selected

Selection only exists inside the Library Tree.

---

# Queue Language

Queue communicates scheduled work.

Queue never communicates active work.

Official queue states:

- Not Queued
- Queued

Queue status should remain visible independently from selection.

---

# Conversion Language

Conversion communicates engine activity.

Official states:

- Idle
- Running
- Completed
- Skipped
- Failed

Only these states are valid in v1.0.

---

# Progress Language

Two independent progress indicators exist.

Batch Progress

Represents overall queue completion.

Current Item Progress

Represents the currently active conversion.

If exact progress is unavailable, use an indeterminate indicator.

Never display fictional percentages.

---

# Console Behavior

The Control Console should always remain visible.

The operator must always know:

What is running.

What is waiting.

What has completed.

What has failed.

Browsing the library must never hide operational information.

---

# Technical Information

Technical metadata is contextual.

It should support the operator.

It should never compete with operational status.

---

# Empty States

When no conversion is active:

Display an explicit Idle state.

When the queue is empty:

Display a clear Empty Queue message.

Never leave empty panels without explanation.

---

# Future Compatibility

This visual language must remain compatible with future versions.

New states may be introduced.

Existing meanings must never change.

# Honest Representation

The interface must only display information that can be truthfully obtained from the backend.

The UI must never simulate operational states.

The UI must never invent progress.

The UI must never estimate values without backend support.

When information is unavailable, the interface should communicate that explicitly.