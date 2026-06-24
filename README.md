# PRISMA 2020 Flow Diagram Generator (Python)

A simple Python script for creating publication-ready **PRISMA 2020 flow diagrams** using only **Matplotlib**.

The script generates a PRISMA-style flowchart with:

* Identification
* Screening
* Eligibility
* Included studies

No PowerPoint, Illustrator, or online tools required.

---

## Features

* Pure Python + Matplotlib
* Publication-ready PNG output
* Easy customisation of:

  * Study counts
  * Database names
  * Exclusion reasons
  * Colours and styling
* No external PRISMA packages required

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/prisma-flow-diagram.git
cd prisma-flow-diagram
```

Install dependencies:

```bash
pip install matplotlib
```

---

## Usage

Run:

```bash
python prisma_flowdiagram.py
```

The figure will be saved as:

```text
prisma_flowdiagram.png
```

---

## Customising Your Diagram

Edit the `COUNTS` dictionary:

```python
COUNTS = {
    "database_results": 251,
    "duplicates_removed": 74,
    "records_screened": 177,
    "records_excluded": 111,
    "full_text_assessed": 66,
    "full_text_excluded": 17,
    "studies_included": 49,
}
```

Update database names:

```python
DB_LINES = [
    "PubMed (n = 104)",
    "Scopus (n = 147)",
]
```

Update exclusion reasons:

```python
REASONS = [
    "No access (n = 14)",
    "Wrong study design (n = 2)",
    "Wrong publication type (n = 1)",
]
```

---

## Output Example

The script generates a PRISMA 2020-style flow diagram as a high-resolution PNG image suitable for:

* Journal articles
* Theses and dissertations
* Conference presentations
* Research reports

---

## Citation

If you use this tool in academic work, please cite the repository.

---

## License

MIT License.
