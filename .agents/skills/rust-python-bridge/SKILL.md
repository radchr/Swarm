---
name: rust-python-bridge
description: >-
  Develop, build, and debug hybrid Python + Rust projects using PyO3, Maturin, and Cargo workspaces.
  Use when creating native Rust extension modules for Python, handling GIL release (py.allow_threads),
  converting types between Rust and Python, configuring maturin builds, or optimizing FFI performance.
---

# Rust-Python Bridge (PyO3 + Maturin) Runbook

This skill provides step-by-step guidance for engineering high-performance Python extensions written in Rust.

---

## 1. Project Architecture (Separation of Concerns)

Always keep the core algorithm separate from the PyO3 binding layer:

```text
├── Cargo.toml (Workspace Root)
├── pyproject.toml (Build configuration with maturin)
├── crates/
│   ├── bevy_engine/      # PURE RUST: No PyO3 dependencies. Testable via `cargo test`.
│   └── bevy_pyo3/        # FFI ADAPTER: Translates between Python objects and bevy_engine.
└── python/
    └── bevy_core/        # Pure Python ergonomics, type stubs, documentation, UI.
```

### Why this separation matters:
1. **Fast Rust Testing:** `bevy_engine` compiles rapidly without Python header dependencies.
2. **Reusability:** The engine crate can be consumed by other Rust projects or CLI binaries.
3. **Clean Boundaries:** Memory conversion and Python error handling live strictly in the FFI crate.

---

## 2. Writing PyO3 Functions & Releasing the GIL

```rust
use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;
use bevy_engine::compute_heavy_workload;

#[pyfunction]
pub fn fast_process<'py>(py: Python<'py>, data: Vec<f32>) -> PyResult<Vec<f32>> {
    if data.is_empty() {
        return Err(PyValueError::new_err("Input data array cannot be empty"));
    }

    // Release GIL for CPU-intensive parallel work
    let result = py.allow_threads(move || {
        compute_heavy_workload(&data)
    });

    Ok(result)
}

#[pymodule]
fn _core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(fast_process, m)?)?;
    Ok(())
}
```

---

## 3. Fast Build & Iteration Loop with Maturin

To compile the Rust crate and update the Python environment in milliseconds:

```bash
# Debug build (fast compile, with debug assertions)
uv run maturin develop

# Optimized release build (SIMD, LTO, maximum throughput)
uv run maturin develop --release
```

---

## 4. Troubleshooting Common Issues

| Symptom | Cause | Solution |
| :--- | :--- | :--- |
| **`ImportError: DLL load failed` on Windows** | Missing VC++ runtime or incompatible Python ABI. | Ensure `maturin develop` is run with the active `.venv` Python. |
| **UI freezes during computation** | GIL was not released in Rust. | Wrap calculation in `py.allow_threads(...)`. |
| **Rust `panic!` terminates Python process** | Unhandled unwrapping in Rust. | Convert all errors to `PyResult` using `map_err(|e| PyValueError::new_err(e.to_string()))`. |
| **IDE shows unresolved reference for Rust function** | Missing `.pyi` type stub. | Add function definition to `_core.pyi`. |
