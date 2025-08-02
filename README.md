# **Text Ranking Tool**

> A lightweight academic research utility for comparative text analysis using recursive median and tournament-based ranking algorithms. Designed for reproducibility and simplicity, it supports both command-line execution and GUI-free workflows.

---

## 🚀 Quick Start

For researchers who want to **run** the tool:

1. **Download** the latest release from the [Releases](https://github.com/mauriciomm7/text_ranking_tool/releases)
2. **Configure** paths using `config.json`
3. **Add Data**: Place your `.csv` files inside `external_data/`
4. **Run** the executable

📖 [**User Guide →**](docs/USER_GUIDE.md)

---

## 🧑‍💻 Developer Setup

For contributors or those modifying the source:

1. **Clone the repo**:

   ```bash
   git clone https://github.com/mauriciomm7/text_ranking_tool.git
   cd text_ranking_tool
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**:

   ```bash
   python src/text_ranking_tool/main.py
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
├── LICENSE                 # ✅ MIT License
└── README.md
```

---

## 📦 Distribution Layout

After downloading from [Releases](https://github.com/mauriciomm7/text_ranking_tool/releases), the executable bundle includes:

```
TextRankingTool-[Platform]-v1.0-Complete/
├── TextRankingTool(.exe)       # Executable
├── config.json                 # Runtime configuration
├── external_data/              # Input CSVs
│   ├── mock_data_01.csv
│   └── revu_data_01.csv
├── external_exports/           # Output results
├── internal_data/              # App-generated data
├── internal_exports/           # App-generated exports
└── internal_users/             # Per-user sessions
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

* `user_mapping`: Maps full names to shortened internal IDs
* `user_colors`: Assigns terminal colors (via [Rich](https://github.com/Textualize/rich))

---

## 📄 CSV Input Format

Each `.csv` file must contain the following columns:

| Column    | Description                                |
| --------- | ------------------------------------------ |
| `id`      | Unique identifier for each text entry      |
| `valence` | Sentiment/affective score (e.g., -1 to 1)  |
| `ranking` | Initial ranking score (can be set to 0)    |
| `text`    | The text snippet to be compared and ranked |


## 📄 License

MIT License — see [LICENSE](LICENSE) for full terms.

---

## 🤝 Contributing

Contributions are welcome!

To get started:

* Fork the repo
* Follow the [developer guide](docs/DEVELOPER_GUIDE.md)
* Submit a pull request with a clear description

---

## 👤 Author

**Mauricio Mandujano Manríquez**
GitHub: [@mauriciomm7](https://github.com/mauriciomm7)

---

## 🎓 Citation

If you use this tool in academic research, please cite:

> **Mandujano Manríquez, M.** (2025). *Text Ranking Tool: Academic research tool for ranking text data using recursive median and tournament algorithms*.
> GitHub: [https://github.com/mauriciomm7/text_ranking_tool](https://github.com/mauriciomm7/text_ranking_tool)


```bibtex
@misc{mandujano2025text,
  author       = {Mauricio Mandujano Manríquez},
  title        = {Text Ranking Tool: Academic research tool for ranking text data using recursive median and tournament algorithms},
  year         = {2025},
  howpublished = {\url{https://github.com/mauriciomm7/text_ranking_tool}},
  note         = {GitHub repository}
}
```

---

## 🙏 Acknowledgments

* Built with [Rich](https://github.com/Textualize/rich) for terminal UI
* Packaged via [PyInstaller](https://www.pyinstaller.org/)
* CI/CD automation using GitHub Actions

---

## 🧾 Version History

* **v1.0.0** (2025-08-02): Initial release with recursive median and tournament-based ranking
