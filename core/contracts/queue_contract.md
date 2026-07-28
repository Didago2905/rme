# RME Queue Contract v1.0

## Purpose

The queue is responsible for scheduling media files for sequential conversion.

The queue is a UI-level concept.

It does not modify the ConversionService architecture.

---

## Queue Unit

The canonical queue unit is a single media file.

Examples:

- Episode
- Movie
- OVA
- Special

Series and seasons are selection containers only.

---

## Queue Type

FIFO (First In, First Out)

Files are processed sequentially.

Only one file may be processed at a time.

---

## Add Selected

Selecting items in the Library does NOT enqueue them.

The user must explicitly execute:

Add Selected to Queue

This operation creates a snapshot of the current selection.

Later changes to the library selection do not modify the existing queue.

---

## Duplicate Files

Duplicate paths are ignored.

A file may appear only once in the active queue.

---

## Queue Execution

Start Queue begins processing from the first pending item.

Items are processed sequentially until the queue is empty.

---

## Failure Policy

If a file fails conversion:

- mark as Failed
- continue with the next queued file

The queue must not stop automatically.

---

## Queue Modification

While processing:

New items may be appended to the end of the queue.

Already completed items remain unchanged.

---

## Queue States

Idle

Running

Completed

---

## Application Close

If the application is closed while the queue is running:

The user should receive a confirmation warning.

No automatic resume is required in v1.0.

---

## Out of Scope

Persistent queues

Pause

Resume

Retry

Queue reordering

Priority scheduling

ETA estimation

Multiple concurrent conversions