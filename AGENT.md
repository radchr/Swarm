# 🐝 Swarm: Біоінспірована Ройова Інтелектуальна Система (Python + Rust)

## 📌 Огляд та Візія Проєкту

**Swarm** — це високопродуктивна гібридна дослідницько-інженерна платформа для симуляції, навчання та керування біоінспірованими роями автономних агентів (дронів, роботів). 
Архітектура проєкту базується на поєднанні:
1. **Нейробіологічних моделей комах (Central Complex / Ring Attractor)** — 32-секторні нейродинамічні кільця дрозофіли для без-GPS навігації, інтеграції шляху (path integration) та фазової пам'яті.
2. **Децентралізованого ройового керування** — поведінка зграї без радіозв'язку (vision/optical flow-based), асиметричне лідерство, уникнення зіткнень та польоти в ускладнених просторах (ліси, тунелі).
3. **Гібридного стеку (Rust + Python)** — максимальна обчислювальна швидкість для фізики та нейродинаміки в поєднанні з гнучкістю Python для машинного навчання, когнітивних агентів (LLM) та аналітики.

---

## 🛠️ Гібридна Архітектура: uv + Cargo (PyO3 & Maturin)

Згідно з інженерним регламентом `rust-python-bridge`, проєкт використовує суворе розділення відповідальностей (**Separation of Concerns**):

```text
Swarm/
├── .env.example                # Шаблон змінних середовища (секрети НЕ комітяться!)
├── .gitignore                  # Захист .env, build-артефактів, .venv, target/
├── AGENT.md                    # Опис місії, архітектури та плану агентів
├── Cargo.toml                  # Workspace Root для Rust
├── pyproject.toml              # Керування Python-проєктом через uv + maturin build-backend
│
├── crates/                     # RUST WORKSPACE
│   ├── swarm_core/             # PURE RUST (Без PyO3):
│   │   │                       # - 32-секторний Ring Attractor (Central Complex)
│   │   │                       # - 2D/3D просторовий індекс (k-d tree, grid partitioning)
│   │   │                       # - Фізичний інтегратор та контактні сили
│   │   │                       # - Швидкі тести: `cargo test`
│   │   └── Cargo.toml
│   │
│   └── swarm_pyo3/             # FFI ADAPTER (PyO3 + Maturin):
│       │                       # - Трансляція типів між Rust та Python
│       │                       # - Звільнення GIL (py.allow_threads) для багатопоточності Rayon
│       │                       # - Двосторонній виклик (Python -> Rust та Rust -> Python)
│       └── Cargo.toml
│
└── python/                     # PYTHON PACKAGE (uv)
    └── swarm/
        ├── __init__.py         # Експорт публічного API
        ├── _core.pyi           # Type hints (анотації) для скомпільованого Rust-модуля
        ├── agents/             # Когнітивні агенти, LLM-інтеграція, стратегічне планування
        ├── env/                # Gymnasium-сумісні середовища для RL-навчання
        └── viz/                # Телеметрія, 2D/3D візуалізація сцени
```

---

## 🔄 Двосторонній Виклик (Bidirectional Interoperability)

### 1. Python ➡️ Rust (Швидкі обчислення)
- Python викликає чисельне ядро симуляції через PyO3:
  ```python
  from swarm._core import SwarmSimulation, SimConfig
  
  sim = SwarmSimulation(num_agents=500, arena_size=(100.0, 100.0))
  # Виконується на всіх ядрах CPU в Rust без блокування GIL:
  sim.tick(dt=0.01)
  positions = sim.get_positions_numpy()  # Zero-copy через buffer protocol
  ```

### 2. Rust ➡️ Python (Когнітивні хуки та зворотні виклики)
- Rust-симулятор під час тику може викликати високорівневі Python-функції (наприклад, оцінка поведінки нейромережею PyTorch або LLM-агентом):
  ```rust
  // Збереження Python-колбека в Rust:
  #[pyclass]
  pub struct AgentController {
      callback: Py<PyAny>,
  }
  
  // Виклик Python-коду з Rust за потреби (з отриманням GIL):
  Python::with_gil(|py| {
      let args = (agent_id, sensor_readings);
      callback.call1(py, args)
  })?;
  ```

---

## ⚡ Робочий Процес розробника (Workflow)

1. **Керування віртуальним середовищем та залежностями**:
   - Python: `uv venv`, `uv add <dependency>`
   - Rust: `cargo add <crate> --package swarm_core`

2. **Компіляція FFI мосту**:
   - Швидка налагоджувальна збірка: `uv run maturin develop`
   - Оптимізована релізна збірка (SIMD, LTO): `uv run maturin develop --release`

3. **Тестування**:
   - Автономні тести ядра Rust: `cargo test --workspace` (миттєве виконання)
   - Інтеграційні тести Python: `uv run pytest`

---

## 🛡️ Безпека та Секрети
- Файл `.env` **строго ігнорується** git і ніколи не потрапляє до репозиторію.
- Усі API ключі (Gemini, Exa, Tavily тощо) зчитуються виключно через безпечне оточення у рантаймі.
- Надано публічний `.env.example` без конфіденційних даних.

---

## 📋 Поточний Статус та Подальші Кроки
- [x] Ініціалізація Git та надійний `.gitignore`.
- [x] Створення шаблону `.env.example`.
- [x] Формування архітектурного опису `AGENT.md`.
- [ ] Узгодження плану реалізації (Implementation Plan).
- [ ] Генерація базового `Cargo.toml` (workspace) та `pyproject.toml` (maturin).
- [ ] Перенесення та оптимізація 32-секторного Ring Attractor у `swarm_core`.
- [ ] Реалізація FFI зв'язки у `swarm_pyo3` та Python-обгортки у `swarm`.
