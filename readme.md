# UAV Component Validation Module

**One‑click electrical compatibility & mission‑performance checks for UAV part combinations.** This repository provides:

- A rule‑based **Compatibility Checker** that verifies electrical fit (battery↔ESC↔motor↔payload, etc.).
- A physics‑backed **Performance Estimator** that scores a component set against mission requirements.
- A minimal **Flask UI + REST API** so you can test combos in a browser *or* script it from build pipelines.

---

## ✨ Quick Start (five commands)

```bash
# 1 · Unpack (or git clone) ----------------------------------
unzip BNT---Component-Validation-Module--main.zip
cd "Component Validation/uav_component_estimator"  # <— project root

# 2 · Create & activate an isolated env -----------------------
python -m venv .venv && source .venv/bin/activate    # PowerShell: .venv\Scripts\Activate

# 3 · Install the exact package set --------------------------
pip install --upgrade pip
pip install -r requirements.txt

# 4 · Smoke‑test the checker ---------------------------------
python -m estimator.quicktest   # prints PASS/FAIL table

# 5 · Launch the mini‑UI -------------------------------------
python app.py                   # open http://127.0.0.1:5000/
```

---

## 1 · Prerequisites

| Tool             | Version         | Notes                                             |
| ---------------- | --------------- | ------------------------------------------------- |
| Python           | **3.10 – 3.12** | Official installers or `brew install python@3.12` |
| Git *(optional)* | latest          | Only needed if you clone instead of unzip         |

> No C/Fortran system libraries required – pure‑Python deps only.

---

## 2 · Project Structure

```
uav_component_estimator/
├── app.py                # Flask entry‑point
├── estimator/            # Core library (compatibility, performance, utils)
├── data/                 # Inventory CSVs (do **not** edit – treat as source‑of‑truth)
├── requirements.txt      # Locked dependency versions
└── README.md             # <— you are here
```

---

## 3 · Command‑line Smoke Test

```bash
python - << 'PY'
from estimator import load_components, check_component_compatibility
from estimator.utils import CSV_PATHS, list_components

ids = {cat: list_components(path)[0] for cat, path in CSV_PATHS.items()}
comps = load_components(ids)

ok, log = check_component_compatibility(comps, detailed=True)
print("COMPATIBLE:", ok)
print("\n".join(log))
PY
```

Expected output starts with `COMPATIBLE: True` followed by a rule‑by‑rule PASS/SKIP breakdown.

---

## 4 · Local Flask UI

```bash
python app.py
```

- Binds to [**http://127.0.0.1:5000/**](http://127.0.0.1:5000/)
- Auto‑reloads on code changes
- Features dropdown selectors populated from `data/` CSVs and a JSON textbox for mission profiles.

Use **Ctrl +C** to stop.

---

## 5 · REST API Reference

### 5.1 List component IDs in a category

```bash
GET /api/components/<category>
# example
curl http://127.0.0.1:5000/api/components/battery
```

### 5.2 Run the Compatibility Checker

```bash
POST /api/check
{
  "battery":   "BAT-123",
  "esc":       "ESC-30A",
  "motor":     "EDF-50mm",
  "propeller": "PROP-9x6"
}
```

Sample response:

```json
{
  "compatible": true,
  "links": { "battery": "https://…", "esc": "https://…" },
  "reasons": [
    "[PASS] Battery voltage within every load’s range",
    "[SKIP] No regulator present",
    "[PASS] Battery 300 A ≥ est. draw 245 A (margin 10%)"
  ]
}
```

### 5.3 Full Performance Evaluation

```bash
POST /api/evaluate
{
  "components": {
    "battery": "BAT-123",
    "esc":     "ESC-30A",
    "motor":   "EDF-50mm"
  },
  "mission": {
    "payload_mass_kg":      0.8,
    "cruise_speed_m_s":    14,
    "endurance_min":       25,
    "takeoff_distance_m":  40
  }
}
```

Returns an object containing computed metrics and an overall `score`.

---

## 6 · Testing

```bash
pip install pytest
pytest            # zero tests for now – add yours in tests/
```

---

## 7 · Contributing

Pull requests are welcome! Please open an issue to discuss major changes first and ensure new logic ships with unit tests.

---

## 8 · License

Released under the **MIT License** – see [`LICENSE`](LICENSE) for details.

