---
name: marimo
description: >-
  Create, edit, analyze, and troubleshoot reactive Python notebooks and web applications using marimo.
  Use when the user mentions marimo, asks to create or edit a marimo notebook (.py), build reactive data apps
  or dashboards, use mo.ui or mo.sql, convert between Jupyter (.ipynb) and marimo, or pair-program on a
  reactive Python notebook in real time.
---

# Marimo: Reactive Notebooks & Agent Pair Programming

Marimo is an open-source, reactive Python notebook that stores notebooks as clean, git-friendly pure Python (`.py`) scripts. Unlike legacy Jupyter notebooks, marimo models computation as a Directed Acyclic Graph (DAG) based on variable definitions and references.

---

## 1. Agent-Human Pair Programming Protocol

When pair-programming on marimo notebooks with a human user:

1. **Hot Reloading Architecture**:
   - The user runs `marimo edit notebook.py` in their browser.
   - The agent modifies `notebook.py` directly using filesystem edit tools.
   - Marimo watches the file on disk and automatically hot-reloads cell code in the browser while preserving execution and UI state whenever possible.

2. **Non-Destructive Cell Modification**:
   - Always preserve the outer structure (`import marimo`, `app = marimo.App(...)`, `@app.cell`, and `if __name__ == "__main__": app.run()`).
   - When adding a new feature or calculation, prefer creating a **new `@app.cell`** instead of stuffing multiple unrelated operations into an existing cell.
   - Keep cells focused: one cell for data loading, one cell for UI controls, one cell for computation/transformation, and one cell for presentation/plotting.

3. **Validation & Linting**:
   - After creating or editing a notebook, you can check syntax or run tests:
     ```bash
     python notebook.py  # executes headlessly as a script
     ```
   - Ensure there are no duplicate global variable definitions across cells.

---

## 2. Core Reactivity & DAG Rules (CRITICAL FOR AI AGENTS)

Marimo statically inspects cells to find **definitions** (globals created) and **references** (globals read). Violating these rules causes `MultipleDefinitionError` or cycle errors.

### Rule 1: No Variable Shadowing / Redeclaration
> [!IMPORTANT]
> **A global variable can only be defined in ONE cell.**
> If `df = pd.read_csv(...)` is in Cell 1, you CANNOT write `df = df.filter(...)` in Cell 2.
> Instead, name the derived variable differently: `filtered_df = df.filter(...)`.

### Rule 2: Private Variables Use Leading Underscore (`_`)
If a variable is an internal helper, iterator, or temporary object that should **not** become part of the global DAG, prefix it with `_`:
```python
@app.cell
def _(df):
    # _temp and _col will not be registered as global DAG nodes
    _temp = []
    for _col in df.columns:
        _temp.append(_col.strip().lower())
    clean_columns = tuple(_temp)
    return (clean_columns,)
```

### Rule 3: UI Element Value Access in Downstream Cells
> [!WARNING]
> **Never read `ui_element.value` in the same cell that defines `ui_element`.**
> Marimo cannot reactively re-run the creation cell on input change without infinite loops.

```python
# Cell 1: Define UI element
@app.cell
def _(mo):
    slider = mo.ui.slider(start=1, stop=100, value=25, label="Threshold")
    slider  # Display the slider
    return (slider,)

# Cell 2: Consume UI element value
@app.cell
def _(df, slider):
    filtered = df[df["score"] >= slider.value]
    filtered
    return (filtered,)
```

### Rule 4: Mutable State Requires `mo.state()`
Do not mutate global lists or dicts in place across cells. Use `mo.state()` to create reactive getters and setters:
```python
@app.cell
def _(mo):
    get_count, set_count = mo.state(0)
    btn = mo.ui.button(label="Increment", on_change=lambda _: set_count(lambda v: v + 1))
    return btn, get_count, set_count

@app.cell
def _(get_count):
    # Automatically re-runs whenever set_count is invoked
    f"Current count: {get_count()}"
```

---

## 3. Standard Marimo Notebook Anatomy

Every marimo notebook file is a valid Python script with this structure:

```python
import marimo

__generated_with = "0.11.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl
    import plotly.express as px
    return mo, pl, px


@app.cell
def _(mo):
    mo.md(
        """
        # Interactive Sales Dashboard
        Filter data dynamically using the reactive controls below.
        """
    )
    return


@app.cell
def _(pl):
    raw_data = pl.DataFrame({
        "category": ["A", "B", "C", "A", "B", "C"],
        "sales": [120, 250, 90, 180, 310, 140],
        "quarter": ["Q1", "Q1", "Q1", "Q2", "Q2", "Q2"],
    })
    return (raw_data,)


@app.cell
def _(mo, raw_data):
    categories = sorted(raw_data["category"].unique().to_list())
    dropdown = mo.ui.dropdown(
        options=["All"] + categories,
        value="All",
        label="Select Category"
    )
    dropdown
    return categories, dropdown


@app.cell
def _(dropdown, px, raw_data):
    filtered_data = (
        raw_data if dropdown.value == "All"
        else raw_data.filter(raw_data["category"] == dropdown.value)
    )
    
    fig = px.bar(
        filtered_data.to_pandas(),
        x="quarter",
        y="sales",
        color="category",
        barmode="group",
        title=f"Sales Overview ({dropdown.value})"
    )
    fig
    return fig, filtered_data


if __name__ == "__main__":
    app.run()
```

---

## 4. Rich UI Elements & Layouts (`mo.ui`)

Marimo provides first-class reactive components:

### Common Inputs
- **Numbers / Sliders**: `mo.ui.slider(1, 100)`, `mo.ui.range_slider(0, 10, value=[2, 8])`, `mo.ui.number(start=0, stop=1000)`
- **Selection**: `mo.ui.dropdown(options=[...])`, `mo.ui.multiselect(options=[...])`, `mo.ui.radio(options=[...])`, `mo.ui.checkbox(label="...")`
- **Text & Code**: `mo.ui.text(placeholder="Search...")`, `mo.ui.text_area()`, `mo.ui.code_editor(language="python")`
- **Data & Tables**: `mo.ui.table(data=df, selection="multi", pagination=True)`
- **Date & File**: `mo.ui.date()`, `mo.ui.file(filetypes=[".csv", ".parquet"])`
- **Interactive Chat**: `mo.ui.chat(model=..., prompts=[...])`

### Layout Containers
Organize elements cleanly using layout utilities:
```python
@app.cell
def _(mo, dropdown, slider, date_picker):
    # Horizontal row with equal or custom spacing
    controls = mo.hstack([dropdown, slider, date_picker], justify="start", gap=1)
    
    # Vertical column
    card = mo.vstack([
        mo.md("### Filter Settings"),
        controls
    ])
    
    # Sidebar, tabs, or accordions
    mo.sidebar([mo.md("## Navigation"), dropdown])
    tabs = mo.ui.tabs({"Table": table_view, "Chart": chart_view})
    accordion = mo.accordion({"Advanced Details": advanced_content})
    return card, controls, tabs, accordion
```

---

## 5. Reactive SQL & DataFrames (`mo.sql`)

Marimo has built-in zero-copy SQL powered by DuckDB. DataFrames in local scope can be queried directly:

```python
@app.cell
def _(mo, raw_data):
    # raw_data DataFrame is automatically available inside SQL!
    query_result = mo.sql(
        """
        SELECT 
            category,
            SUM(sales) as total_sales,
            AVG(sales) as avg_sales
        FROM raw_data
        GROUP BY category
        ORDER BY total_sales DESC
        """
    )
    return (query_result,)
```

---

## 6. CLI Reference & Workflows

| Task | Command |
| :--- | :--- |
| **Launch reactive editor** | `marimo edit notebook.py` |
| **Run as web application** | `marimo run notebook.py` |
| **Convert Jupyter to Marimo** | `marimo convert notebook.ipynb -o notebook.py` |
| **Export to Jupyter** | `marimo export ipynb notebook.py -o notebook.ipynb` |
| **Export to flat script** | `marimo export script notebook.py -o script.py` |
| **Export to static HTML (wasm)** | `marimo export html-wasm notebook.py -o dist/` |
| **Headless execution test** | `python notebook.py` |

---

## 7. Common Antipatterns & How to Fix Them

1. **Error: `MultipleDefinitionError: 'x' was defined by another cell`**
   - *Cause:* Two cells define global variable `x`.
   - *Fix:* Rename one variable (e.g., `x_raw` and `x_clean`), or prefix local scratch variables with an underscore `_x`.

2. **Error: `CycleError` (Cyclic Dependency)**
   - *Cause:* Cell A references variable from Cell B, while Cell B references variable from Cell A.
   - *Fix:* Split the logic so data flows unidirectionally in a DAG: Input -> Transform -> Output.

3. **Stale UI element values or non-reactive updates:**
   - *Cause:* Reading `.value` in the same cell that instantiated the UI control.
   - *Fix:* Move all code reading `control.value` into a separate downstream `@app.cell`.
