# **Text Ranking Tool**

> A lightweight academic research utility for comparative text analysis using recursive median and tournament-based ranking algorithms. Designed for reproducibility and simplicity, it supports both command-line execution and GUI-free workflows.

---

## 🚀 Quick Start

For researchers who want to **run** the tool:

1. **Download** the latest release from the [Releases](https://github.com/mauriciomm7/text_ranking_tool/releases)
2. **Configure** paths using `config.json`
3. **Add Data**: Place your `.csv` files inside `external_data/`
4. **Run** the executable

> ⚠️ **Mac binaries are currently unavailable.** Mac users should run from source — see [Developer Setup](#-developer-setup) below.

📖 [**User Guide →**](docs/USER_GUIDE.md)

---

## 📦 Distribution Layout

After downloading from [Releases](https://github.com/mauriciomm7/text_ranking_tool/releases), the executable bundle includes:

```shell
    TextRankingTool-Windows-v1.0-Complete/
    ├── TextRankingTool.exe     # Windows executable
    ├── config.json             # Runtime configuration
    ├── external_data/          # Input CSVs
    │   ├── mock_data_01.csv
    │   └── revu_data_01.csv
    ├── external_exports/       # Output results
    ├── internal_data/          # App-generated data
    ├── internal_exports/       # App-generated exports
```

---

## ⚙️ Configuration (`config.json`)

Sample:

```json
    {
      "install_root": "./",
      "external_data_dir": "external_data",
      "internal_data_dir": "internal_data",
      "external_export_dir": "external_exports",
      "internal_export_dir": "internal_exports",
      "internal_users_dir": "internal_users",
      "algorithm": "recursive_median",
      "available_algorithms": ["recursive_median", "tournament"],
      "default_algorithm": "recursive_median",
      "user_mapping": {
        "Your Name": "YourName",
        "User Beta": "UserBeta",
        "User Alpha": "UserAlpha"
      },
      "user_colors": {
        "Your Name": "bright_blue",
        "User Beta": "bright_magenta",
        "User Alpha": "bright_green"
      },
      "required_columns": ["id", "valence", "ranking", "text"]
    }
```

- `user_mapping`: Maps full names to shortened internal IDs
- `user_colors`: Assigns terminal colors (via [Rich](https://github.com/Textualize/rich))

---

## 🎨 Text Formatting (Optional)

You can configure the tool to visually format specific words or phrases during comparisons. This is useful for de-emphasizing stopwords, flagging known terms, or guiding rater attention.

Add an optional `text_formatting` block to `config.json`:

```json
    {
      "text_formatting": {
        "type": "strike",
        "patterns_file": "external_data/formatting_patterns.txt"
      }
    }
```

If `text_formatting` is absent from the config the tool runs normally with no formatting applied.

### Formatter types

| Type        | Effect                                        |
| ----------- | --------------------------------------------- |
| `strike`    | Strikethrough matched words/phrases           |
| `bold`      | Bold matched words/phrases                    |
| `highlight` | Inverts terminal fg/bg on matched words/phrases |
| `dim`       | Dims matched words/phrases                    |
| `underline` | Underlines matched words/phrases |
| `italic` | Italicises matched words/phrases |


### Patterns file format

A plain `.txt` file, one word or phrase per line:

```txt
  # Lines starting with # are ignored

  however
  therefore
  the results suggest
  it is important to note
```

- Matching is **case-insensitive**
- Both single words and multi-word phrases are supported
- Place the file anywhere inside your distribution and point `patterns_file` to it

---

## 📄 CSV Input Format

Each `.csv` file must contain the following columns:

| Column    | Description                                |
| --------- | ------------------------------------------ |
| `id`      | Unique identifier for each text entry      |
| `valence` | Sentiment/affective score (e.g., -1 to 1)  |
| `ranking` | Initial ranking score (can be set to 0)    |
| `text`    | The text snippet to be compared and ranked |

---

## 🧑‍💻 Developer Setup

For contributors or those modifying the source:

1. **Clone the repo**:

```shell
git clone https://github.com/mauriciomm7/text_ranking_tool.git
cd text_ranking_tool
```

2. **Install dependencies**:

```shell
pip install -r requirements.txt
```

3. **Run the app**:

```shell
python src/text_ranking_tool/main.py
# If fails:     
python -m src.text_ranking_tool.main
```

4. Use the `devroot/` directory for test input/output during development.

📖 [**Developer Guide →**](docs/DEVELOPER_GUIDE.md)

---

## 🧭 Project Structure

```shell
    text_ranking_tool/
    ├── src/
    │   └── text_ranking_tool/
    │       ├── algorithms/     # Ranking algorithms (recursive, tournament)
    │       ├── analysis/       # CLI analysis interface
    │       ├── config/         # Settings, constants
    │       ├── data/           # CSV/data loaders
    │       ├── export/         # Export formats (CSV, JSON, etc.)
    │       ├── ranking/        # Core logic for pairwise ranking
    │       ├── stats/          # Statistics and scoring
    │       ├── utils/          # Utility helpers
    │       ├── ux/             # CLI UX components (Rich)
    │       ├── validation/     # Schema and input checks
    │       └── main.py         # CLI entry point
    │
    ├── packaging/              # Build configs
    │   ├── windows/
    │   └── mac/
    │
    ├── devroot/                # Local test environment
    │   ├── external_data/      # Sample input data
    │   ├── external_exports/   # Output from experiments
    │   └── config.json         # Dev-time override config
    │
    ├── .github/workflows/      # GitHub Actions CI/CD
    ├── config.json             # Global runtime config
    ├── requirements.txt        # Python dependencies
    ├── .gitignore
    ├── LICENSE                 # Research & Commercial License
    └── README.md
```
---

## 📄 License

**Research & Non-Commercial License** — Free for academic, educational, and non-commercial use with attribution

**Commercial License** — Contact `mauriciomm7[at]outlook[dot]com` for commercial licensing approval

See [LICENSE](LICENSE) for full terms.

---

## 🤝 Contributing

Contributions are welcome!


---

## 🎓 Citation

If you use this tool in academic research, please cite:

> **Mandujano Manríquez, M.** (2025). *Text Ranking Tool: Academic research tool for ranking text data using recursive median and tournament algorithms*.
> GitHub: [https://github.com/mauriciomm7/text_ranking_tool](https://github.com/mauriciomm7/text_ranking_tool)

    @misc{mandujano2025text,
      author       = {Mauricio Mandujano Manríquez},
      title        = {Text Ranking Tool: Academic research tool for ranking text data using recursive median and tournament algorithms},
      year         = {2025},
      howpublished = {\url{https://github.com/mauriciomm7/text_ranking_tool}},
      note         = {GitHub repository}
    }

*Note: Commercial use requires separate licensing. Contact the author for commercial permissions.*

---

## 🙏 Acknowledgments

- Built with [Rich](https://github.com/Textualize/rich) for terminal UI
- Packaged via [PyInstaller](https://www.pyinstaller.org/)
- CI/CD automation using GitHub Actions

---

## 🧾 Version History

- **v1.1.0beta** (2026-03-04): Added optional text formatting support (strike, bold, highlight, dim)
- **v1.0.1beta** (2025-08-02): Initial release with recursive median and tournament-based ranking
