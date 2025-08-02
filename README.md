# **Text Ranking Tool**

Academic research tool for ranking text data using recursive median and tournament algorithms.

---

## 🚀 Quick Start

For researchers who want to use the tool:

1. **Download** the latest release from the [Releases](../../releases) page
2. **Configure** paths via `config.json`
3. **Add Data**: Place CSV files in your `external_data/` folder
4. **Run** the executable

📖 [**User Guide →**](docs/USER_GUIDE.md)

---

## 🧑‍💻 Development Setup

For developers who want to modify or contribute:

1. **Clone**:

   ```bash
   git clone https://github.com/mauriciomm7/text_ranking_tool.git
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**:

   ```bash
   python src/text_ranking_tool/main.py
   ```

4. Use the `devroot/` structure for input/output during development.

📖 [**Developer Guide →**](docs/DEVELOPER_GUIDE.md)

---
## 🧭 Project Directory Overview

```shell
text_ranking_tool/
├── src/                   # Application source code
│   └── text_ranking_tool/
│       ├── algorithms/    # Recursive median, tournament, etc.
│       ├── analysis/      # Analysis mode UI
│       ├── config/        # Constants and settings
│       ├── data/          # File and CSV loaders
│       ├── export/        # Export formatters
│       ├── ranking/       # Core comparison and ranking logic
│       ├── stats/         # Statistics calculations
│       ├── utils/         # General-purpose helpers
│       ├── ux/            # UI components (CLI)
│       ├── validation/    # Schema validation
│       └── main.py        # Entry point
│
├── packaging/             # Build configurations
│   ├── windows/           # Windows-specific
│   └── mac/               # macOS-specific
│
├── devroot/               # Local testing environment
│   ├── external_data/     # Sample input data
│   ├── external_exports/  # Sample output results
│   └── config.json        # Runtime override config
│
├── .github/workflows/     # CI/CD GitHub Actions
├── config.json            # Global app config
├── requirements.txt       # Python package dependencies
├── .gitignore             # Git exclusions
├── LICENSE                # ✅ MIT License
└── README.md              # ✅ Enhanced: Attribution + dev info
```

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🤝 Contributing

Contributions are welcome!
To get started, follow the [developer guide](docs/DEVELOPER_GUIDE.md) and submit a pull request.

---

## 👤 Author

**Mauricio Mandujano Manríquez**
GitHub: [@mauriciomm7](https://github.com/mauriciomm7)

---

## 🎓 Citation

If you use this tool in academic research, please cite:

> **Mandujano Manríquez, M.** (2025). *Text Ranking Tool: Academic research tool for ranking text data using recursive median and tournament algorithms*.
> GitHub: [https://github.com/mauriciomm7/text\_ranking\_tool](https://github.com/mauriciomm7/text_ranking_tool)

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
* Cross-platform builds via [PyInstaller](https://www.pyinstaller.org/)
* Automated with GitHub Actions

---

## 🧾 Version History

* **v1.0.0** (2025-08-02): Initial release with recursive median and tournament-based ranking

