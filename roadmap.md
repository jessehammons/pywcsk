# pywcsk Roadmap

A minimal, rigorous roadmap for implementing a Python version of `wc` using Spec Kit.
The goal is **clarity, correctness, and completeness** — not perfect replication of all edge cases.

---

## 🎯 Project Goal

Recreate the core behavior of the Unix `wc` command with:

* Spec-driven development (Spec Kit)
* Strong test coverage (unit, integration, oracle)
* Incremental, well-defined features

---

## ✅ Definition of Done

`pywcsk` is considered complete when:

* All core `wc` flags are implemented (`-l`, `-w`, `-c`)
* Multi-file behavior and totals are correct
* Default output matches `wc` (lines, words, bytes)
* Golden/oracle tests pass against system `wc`
* Spec coverage is complete (`/speckit.analyze` passes)
* No known behavioral mismatches in common usage

---

## 🧭 Feature Roadmap

Each feature should be implemented via:

```text
/specify → /plan → /tasks → /implement → /analyze
```

---

### Phase 1 — Foundation

#### 001: CLI Skeleton ✅

* Click-based CLI
* `--help`, `--version`
* Accept file arguments and stdin

---

#### 002: Line Counting (Default) ✅

* Count `\n` characters
* Default behavior when no flags provided
* Works for files and stdin

---

#### 003: Word Counting (`-w`) ✅

* Count words using whitespace splitting
* Handle:

  * multiple spaces
  * tabs
  * newlines
  * no trailing newline
* Verified with oracle tests against `wc -w`

---

#### 004: Explicit Line Flag (`-l`) ✅

* Add `-l` flag
* Preserve default (no-flag) behavior
* Ensure CLI consistency with `wc`

---

#### 005: Word Splitting Hardening ✅

* Validate behavior with:

  * mixed whitespace
  * punctuation edge cases
* Expand oracle coverage

---

## 🚧 Phase 2 — Core Feature Completion

#### 006: Disallow Multiple Flags (Temporary Guard)

* Reject combinations like `-l -w`
* Exit non-zero with clear error message
* Prevent undefined behavior
* Prepares for future combined output feature

---

#### 007: Byte Counting (`-c`)

* Count raw bytes (`len(data)`)
* Add CLI flag `-c`
* Validate with oracle tests (`wc -c`)
* Distinguish from character count (future `-m`)

---

## 🧩 Phase 3 — Composition & Output

#### 008: Combined Flags (`-l -w -c`)

* Support multiple flags together
* Match `wc` output ordering:

  * lines, words, bytes
* Ensure correct formatting and spacing
* Remove temporary restriction from feature 006

---

#### 009: Default Combined Output

* No flags → print:

  * lines, words, bytes
* Match standard `wc` behavior
* Maintain backward compatibility awareness

---

## 📁 Phase 4 — Multi-file Behavior

#### 010: Multiple Files

* Support:

  ```bash
  pywcsk file1.txt file2.txt
  ```
* Output per file
* Match `wc` formatting and alignment

---

#### 011: Totals Row

* Add final `total` line when multiple files
* Match `wc` behavior exactly
* Include all active counts (l/w/c)

---

## 🧪 Phase 5 — Robustness & Edge Cases

#### 012: Stdin Handling

* No args → read stdin
* Ensure consistent behavior with flags
* Optional: support `-` as stdin

---

#### 013: Newline Edge Cases

* No trailing newline
* Empty file
* Single-line input
* Match `wc` exactly

---

#### 014: Unicode / UTF-8 Handling

* Test with:

  * emoji
  * multibyte characters
  * non-Latin scripts
* Ensure:

  * `-c` counts bytes
  * future `-m` counts characters correctly

---

## 🧪 Testing Strategy

For each feature:

* **Unit tests**: core logic (e.g., counting functions)
* **Integration tests**: CLI behavior
* **Oracle tests**: compare against system `wc`

Golden tests should cover:

* normal inputs
* edge cases
* tricky whitespace
* multi-line input

---

## 🚫 Non-Goals (for this roadmap)

To keep the project focused:

* Perfect parity with all `wc` implementations (BSD/GNU differences)
* Performance optimization for large files
* Locale-specific behavior
* Full POSIX compliance beyond core features

---

## 🧘 Guiding Principles

* Prefer **clarity over completeness**
* Prefer **specification over intuition**
* Prefer **small features over large rewrites**
* Define behavior before implementing it
* Use oracle testing to resolve ambiguity

---

## 🚀 After Completion (Optional Extensions)

* `-m` (character count)
* `-L` (longest line length)
* dynamic column width formatting
* error handling (permissions, missing files)
* performance benchmarking
* fuzz testing vs `wc`

---

## 💡 Summary

This roadmap defines a **finite, high-quality stopping point**:

* ~10–14 features total
* Strong spec/test alignment
* Real-world correctness via oracle testing

Completion means:

> The tool is **correct, tested, and understandable** — not endlessly extended.

---
