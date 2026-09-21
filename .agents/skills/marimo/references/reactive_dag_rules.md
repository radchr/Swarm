# Marimo DAG & Reactive Execution Engine Reference

This reference explains the internal mechanics of marimo's reactive dataflow execution graph and how AI agents should structure code to maintain high performance, reproducibility, and clean pair-programming ergonomics.

---

## 1. How Marimo Builds the DAG

Unlike standard Jupyter kernels (which execute code sequentially in an arbitrary order and maintain an invisible global state dictionary), marimo statically parses the Abstract Syntax Tree (AST) of each cell before executing any code.

For every `@app.cell`, marimo extracts two sets:
- **`defs` (Definitions)**: Global variables, functions, and classes assigned or declared at top-level within the cell.
- **`refs` (References)**: Global symbols accessed within the cell that were not defined locally within that cell.

From these sets, marimo constructs a Directed Acyclic Graph:
- **Nodes**: Individual cells.
- **Edges**: Directed edge from Cell $A \to \text{Cell } B$ if $\text{defs}(A) \cap \text{refs}(B) \neq \emptyset$.

When a cell runs (e.g. user edits code or a reactive UI element triggers an update), marimo identifies all **descendant cells** in the DAG and schedules them for execution in topological order.

---

## 2. Global vs. Local/Private Scope

In Python notebooks, polluting the global namespace causes accidental coupling. In marimo, polluting the global namespace can inadvertently trigger unwanted cell executions.

### Scoping Rules:
1. **Public Globals**: Any variable `var` without a leading underscore is tracked as a global DAG node.
2. **Private Locals**: Any variable `_var` with a leading underscore is scoped strictly to that cell. Marimo ignores it when calculating dependencies.
3. **Internal Functions**: Helper functions intended only for a single cell should be defined with a leading underscore (e.g., `def _format_date(d): ...`) or encapsulated inside a closure.

```python
# Good: Local helpers do not pollute the DAG
@app.cell
def _(df):
    def _normalize(series):
        return (series - series.mean()) / series.std()

    normalized_df = df.with_columns(_normalize(df["sales"]).alias("norm_sales"))
    return (normalized_df,)
```

---

## 3. The Reactivity Flow with `mo.state()`

Standard Python variables cannot trigger re-execution when mutated in-place (e.g. `my_list.append(x)` does not change the identity of `my_list` and cannot be tracked statically).

When dynamic application state must change across user interactions:
1. Create state with `get_val, set_val = mo.state(initial_value)`.
2. Assign `get_val` and `set_val` to global names.
3. Any cell that invokes `get_val()` is automatically registered as an observer.
4. When `set_val(new_val)` is called (e.g., in a button's `on_change` or an event callback), marimo re-runs all observer cells.

```python
@app.cell
def _(mo):
    get_history, set_history = mo.state([])
    
    def on_submit(text):
        if text:
            set_history(lambda prev: prev + [text])

    input_box = mo.ui.text(placeholder="Type a message...", on_change=on_submit)
    return get_history, input_box, on_submit, set_history

@app.cell
def _(get_history, mo):
    # This cell automatically updates whenever on_submit pushes to state
    history_items = [mo.md(f"- {msg}") for msg in get_history()]
    mo.vstack(history_items)
```

---

## 4. Seamless Agent Pair-Programming Loop

When working as an AI agent alongside a human developer in marimo:

1. **Keep the Editor Open**: The user should leave `marimo edit app.py` running in their terminal/browser.
2. **File Modifications**: The agent edits `app.py` directly.
3. **Live Sync**: Marimo uses file system watchers to detect changes. The instant the agent writes changes to `app.py`, the user's browser updates the cell code in place.
4. **Topological Coherence**: 
   - Never generate cyclic dependencies ($A \to B \to A$).
   - Never create cells that attempt to delete globals (`del var`).
   - Group imports in an early cell so dependencies are clearly visible.
5. **Wasm and Web Deployment**:
   - Notebooks designed with marimo can be instantly packaged into standalone static HTML applications (`marimo export html-wasm app.py -o dist/`), which can run entirely client-side via Pyodide without a Python backend!
