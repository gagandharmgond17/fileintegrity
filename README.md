# File Integrity Monitor

A beginner-friendly Python cybersecurity project that detects file changes using SHA-256 hashes.

## Features

- Creates a baseline of files in a folder.
- Detects newly added files.
- Detects modified files.
- Detects deleted files.
- Uses Python's built-in libraries only (no third-party dependencies).

## Requirements

- Python 3.9 or newer

## Run it

Open a terminal in this project folder.

### 1. Add files to monitor

Place test files inside the `monitored/` folder.

### 2. Create the initial baseline

```bash
python main.py --init
```

This stores the SHA-256 hash of every file in `baseline.json`.

### 3. Make a change

Edit a file, add a new file, or delete a file inside `monitored/`.

### 4. Check for changes

```bash
python main.py
```

The report will show `[NEW]`, `[MODIFIED]`, and `[DELETED]` entries.

### Monitor a different folder

```bash
python main.py --target "C:\Users\YourName\Documents\TestFolder" --init
python main.py --target "C:\Users\YourName\Documents\TestFolder"
```

## Example output

```text
=== File Integrity Report ===
[NEW]      notes.txt
[MODIFIED] config.txt
[DELETED]  old_backup.txt

Summary: 1 new, 1 modified, 1 deleted.
```

## How it works

1. The program reads each file as bytes.
2. It calculates a SHA-256 digest with `hashlib`.
3. It stores file paths and hashes in a JSON baseline.
4. On the next run, it calculates the hashes again and compares snapshots.
5. Differences indicate added, modified, or deleted files.

## Security notes

- A hash change indicates that file content changed; it does not explain whether the change was malicious.
- Store a trusted copy of the baseline somewhere an attacker who can modify the monitored folder cannot also alter.
- This starter version is a manual scanner, not a real-time monitoring agent.
- SHA-256 is used for integrity checking, not password storage.

## Possible improvements

- Add scheduled scans.
- Export reports to CSV.
- Add file type filters.
- Add a simple graphical interface.
- Send alerts when changes are detected.

## License

MIT
