<div align="center">

# 📄 Simple Log Reader

### Find errors and warnings in your text logs.

A small Python desktop app that opens a log file and makes important messages easy to spot.

</div>

---

## What it does

- Opens `.txt` log files.
- Finds lines containing `ERROR` or `WARNING` (uppercase or lowercase).
- Shows each match with its line number.
- Displays error and warning totals.
- Filters the view to all messages, errors, or warnings.

## Start the app

You need **Python 3.10 or newer**. No extra packages are needed.

Open a terminal in this folder and run:

```bash
python main.py
```

On Windows, `py main.py` works if the Python launcher is installed.

## Use it

1. Select **Open log file**.
2. Choose a `.txt` log file.
3. Select **All**, **Error**, or **Warning** to filter the results.

Press `Ctrl + O` to open another file.

## Files

```text
Simple-Log-Reader/
├── main.py      # The desktop app
└── README.md    # This guide
```

## Notes

The app reads the selected file on your computer. It does not upload the log anywhere.
