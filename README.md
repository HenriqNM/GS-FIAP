# Telemetry Analysis Engine

A modular system designed for processing, statistical analysis, validation, and graphical visualization of telemetry data streams utilizing moving averages.

---

## Team Members

* **Henrique Nunes Mororó** — RM 574073
* **Bernardo de Paula Rodrigues** — RM 572376
* **Arthur Moreira Costa** — RM 571532

---

## System Architecture

The project is structured into independent modules with strict separation of concerns:

* **`app.py` (Execution):** The system entry point. Orchestrates the execution flow by loading configurations, invoking the data processor, handling user interaction, and triggering graph generation.
* **`motor.py` (Core Engine):** Implements the `MotorAnalise` class. Manages the volatile history of sensor states, calculates moving averages over a fixed window of the last 3 readings, and dynamically resolves validation rules via reflection (`getattr`).
* **`regras.py` (Validation Layer):** Defines the `RegraValidacao` abstract base class (ABC) and specific analytical algorithms:
  * `ValidacaoLimiteSimples`: Linear range validation (Normal, Alert, Critical).
  * `ValidacaoLimiteDuplo`: Bimodal validation for sensors operating within a central optimal range with upper and lower boundary thresholds.
* **`processo.py` (Data Processing):** Consumes raw telemetry logs, tracks hardware message sequences, and structures cleaned time-series data optimized for visualization.
* **`interface.py` (User Interface):** Manages interactive terminal menus. Dynamically lists available operational sensors and implements defensive validation against invalid operator inputs.
* **`graphic.py` (Visualization):** Renders sequential line charts using `matplotlib` based on the processed time-series metrics of the selected sensor.
* **`dados.py` (Data Source):** Simulates real-time telemetry data streams, containing standard operational readings and corrupted payloads for system stress testing.

---

## Technical Highlights

* **Defensive Programming:** Granular exception handling targeting `ValueError`, `KeyError`, `TypeError`, and `AttributeError`. The application isolates malformed payloads—such as invalid string states, incorrect array structures, or unconfigured sensors—without disrupting overall system execution.
* **Optimized Memory Footprint:** Utilizes `collections.deque(maxlen=3)` to maintain sliding window telemetry buffers per sensor, ensuring $O(1)$ insertion complexity and automated eviction of obsolete data points.
* **Strict Type Hinting:** Codebase fully annotated with Type Hints verified via `mypy` to enforce structural integrity across method signatures, safeguard return values, and dynamic instances.
* **Time-Series Integrity:** Implements active filtering in the data pipeline to prevent corrupted records (`"Dado corrompido"`) from injecting null parameters or structural fallbacks (e.g., `0.0`) into the datasets, eliminating statistical distortion in trend lines.
* **Refined Terminal UI:** Employs standardized ANSI escape sequences exclusively for critical boundaries, section headers, and dynamic operational states (`Normal`, `Alerta`, `CRÍTICO`), enhancing operator scannability without visual clutter.
* **Boundary Testing:** Includes an automated test suite driven by `unittest` designed to validate strict inequality limits ($>$ and $<$) under precise floating-point operations.
