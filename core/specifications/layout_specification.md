# RME Layout Specification v1.0

## Purpose

This document defines the physical layout of the RME main window.

It describes where interface elements live.

It does not define behavior.

Behavior is defined by the contracts.

---

# Main Window

The application is divided into two primary regions.

+----------------------------+-----------------------------+
|                            |                             |
|                            |                             |
|        Library             |      Control Console        |
|                            |                             |
|                            |                             |
+----------------------------+-----------------------------+

The Library is the primary workspace.

The Control Console is permanently visible.

---

# Header

A compact information bar located at the top of the application.

Displays only:

- Application Name
- Version
- Active Library

No operational commands belong here.

---

# Library Panel

The Library occupies the left side.

Contains:

- Library Tree
- Hierarchical Selection
- Library Commands

Library Commands:

- Open Library
- Refresh Library
- Add Selected to Queue

---

# Control Console

The Control Console occupies the right side.

Contains the following sections in priority order:

1. Current Activity

2. Queue

3. Batch Progress

4. Current Item Progress

5. Selected Item Summary

Sections may be collapsible.

The Current Activity section must always remain visible.

---

# Window Behavior

The Control Console remains visible while browsing.

Selecting different files updates only the Selected Item Summary.

Browsing must never hide queue or conversion information.

---

# Future Compatibility

Additional console sections may be introduced in future versions.

The two-column layout should remain the primary application layout.