# Hivenet MCP Server - Build and Implementation Documentation

This document summarizes the steps taken to implement, debug, and package the Hivenet MCP (Model Context Protocol) server into a standalone executable.

## 📋 Project Overview
The project is a Python-based MCP server that connects to a **Cube.js** analytics API. It provides tools for Claude to interact with data models, retrieve metadata, and execute queries.

### Tech Stack
- **Python 3.14**: Executing in a Windows environment.
- **FastMCP**: A framework for building MCP servers quickly.
- **PyInstaller**: Used for packaging the script into a single `.exe`.
- **Cube.js**: The backend data platform providing the analytics API.

---

## 🛠️ Implementation Steps

### 1. Code Fixes & Refactoring
- **Typo Corrections**: 
  - Fixed `duckbd` to `duckdb` in `duckdb_engine.py`.
  - Renamed `requirments.txt` to `requirements.txt`.
- **Dependency Management**: Installed missing dependencies including `mcp`, `requests`, `pandas`, `typer`, and `anyio`.

### 2. Packaging Challenges (The "PyInstaller vs. Nuitka" Saga)
We attempted multiple ways to package the application to ensure it runs without a Python environment installed on the target machine.

#### Attempt 1: Standard PyInstaller
- **Issue**: Initial attempts failed because `python -m pyinstaller` is case-sensitive (`python -m PyInstaller` is required).
- **Issue**: The `mcp` library uses dynamic imports that PyInstaller often misses.

#### Attempt 2: Nuitka (The "Professional" Solution)
- **Concept**: Nuitka compiles Python to C++ for better performance and import handling.
- **Result**: **FAILED (Segmentation Fault)**.
- **Reason**: Python 3.14 is currently in an alpha/experimental state. Nuitka relies on low-level Python internals which are unstable in this version, leading to memory corruption (Segfault) during execution.

#### Attempt 3: Advanced PyInstaller (Final Solution)
- **Command used**:
  ```powershell
  python -m PyInstaller --onefile --name hivenet-mcp --collect-all mcp --hidden-import=anyio._backends._asyncio --clean server.py
  ```
- **Why this worked**: 
  - `--collect-all mcp`: Ensures all metadata, schemas, and subpackages of the MCP library are included.
  - `--hidden-import=anyio._backends._asyncio`: Explicitly includes the asynchronous backend required by FastMCP that PyInstaller's static analysis misses.
  - Moved from Nuitka back to PyInstaller as it is more resilient to the experimental Python 3.14 structures.

---

## 🚀 Deployment & Configuration

### Executable Location
The final executable is located at:
`F:\Hivenet\mcp-server\dist\hivenet-mcp.exe`

### Claude Desktop Integration
The `claude_desktop_config.json` was updated to point directly to the executable. This allows Claude to run the server without needing to manage Python paths or virtual environments.

**Current Configuration:**
```json
{
  "mcpServers": {
    "hivenet": {
      "command": "F:\\Hivenet\\mcp-server\\dist\\hivenet-mcp.exe"
    }
  }
}
```

---

## 🔍 TroubleShooting & Notes
- **Case Sensitivity**: Always use `PyInstaller` (capital P, capital I) when calling via `python -m`.
- **Python 3.14**: This is a very new version. If you experience further instability, downgrading to **Python 3.12** is recommended for better library compatibility.
- **Zstandard Warning**: During build, you may see a warning about `zstandard`. This just means the binary is slightly larger (uncompressed) but functions perfectly.
