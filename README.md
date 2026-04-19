# FanFolder

**Turn any folder into a beautiful Mac-style fan on your Windows taskbar.**

FanFolder brings the macOS Dock "Fan" folder experience to Windows. Pin any folder to the taskbar, click it, and watch your most recent files bloom out in an animated arc — ready to open, drag, or right-click with the full Windows shell context menu.

🌐 **Website:** <https://olebhartvigsen.github.io/FanFolder/>
⬇️ **Download:** [Latest release](https://github.com/olebhartvigsen/FanFolder/releases/latest)

---

## Features

- **Animated fan popup** — choose from Spring, Fan, Glide, Fade, or None
- **Any folder, any time** — Downloads, Desktop, Screenshots, projects, whatever you use most
- **Fully interactive** — open with one click, drag files into any app, right-click for the full shell menu
- **Smart sorting & filtering** — by date or name, show/hide folders, optional regex filename filter
- **Native Windows icons** — high-resolution file icons via the Windows Shell
- **Lightweight** — ~160 KB executable, no admin rights required, no background services
- **Free for life** — see [LICENSE](LICENSE)

---

## Install

### Winget (recommended)

```powershell
winget install OleBhartvigsen.FanFolder
```

### Direct installer

Download `FanFolderSetup.exe` from the [latest release](https://github.com/olebhartvigsen/FanFolder/releases/latest) and run it. No admin rights required.

---

## System requirements

| | |
|---|---|
| **OS** | Windows 10 (1809+) or Windows 11 |
| **Architecture** | x64 and ARM64 |
| **Runtime** | Microsoft Visual C++ 2015–2022 Redistributable (bundled in installer) |
| **Disk** | ~1 MB |
| **Memory** | ~15 MB idle |

---

## Technical overview

FanFolder is a native Win32/C++20 desktop application.

- **Language:** C++20
- **UI:** Win32 + GDI+ (layered windows, DWM iconic thumbnails)
- **Shell integration:** `IShellItemImageFactory` for icons, OLE drag-and-drop, `IContextMenu` for right-click
- **Configuration:** `HKCU\SOFTWARE\FanFolder` registry keys (`FolderPath`, `SortMode`, `MaxItems`, `AnimationStyle`, `FilterRegex`, …)
- **Build:** CMake + MSVC (Visual Studio 2022, C++ desktop workload)
- **Installer:** Inno Setup, single-file `FanFolderSetup.exe` per architecture
- **Distribution:** GitHub Releases + winget community repository

Source code is maintained in a private repository. This repository (`FanFolder`) is the public distribution channel and hosts the website, releases, and winget manifests.

---

## Configuration

All settings are available from the tray-icon menu, or directly via the registry at `HKCU\SOFTWARE\FanFolder`:

| Value | Type | Default | Description |
|-------|------|---------|-------------|
| `FolderPath` | REG_SZ | Downloads | Folder to display |
| `SortMode` | REG_SZ | `DateModifiedDesc` | Sort order (`DateModifiedDesc`, `DateModifiedAsc`, `DateCreatedDesc`, `DateCreatedAsc`, `NameAsc`, `NameDesc`) |
| `MaxItems` | REG_DWORD | `15` | Items shown in the fan (5–25) |
| `IncludeDirectories` | REG_DWORD | `1` | Include subfolders |
| `ShowExtensions` | REG_DWORD | `0` | Show file extensions in labels |
| `FilterRegex` | REG_SZ | *(empty)* | Optional filename filter |
| `AnimationStyle` | REG_SZ | `Spring` | `Fan`, `Glide`, `Spring`, `Fade`, or `None` |

---

## License

FanFolder is **free for personal and commercial use, forever**. The source code is not public.

See [LICENSE](LICENSE) for the full terms.

---

## Support

- 🐛 **Report a bug / request a feature:** [Issues](https://github.com/olebhartvigsen/FanFolder/issues)
- 🌐 **Website:** <https://olebhartvigsen.github.io/FanFolder/>

---

© 2026 Ole Bulow Hartvigsen. All rights reserved.
