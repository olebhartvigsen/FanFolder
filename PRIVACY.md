# FanFolder Privacy Notice

Copyright (c) 2026 Ole Bülow Hartvigsen. All rights reserved.

Last updated: 31 July 2026

FanFolder is a local Windows taskbar utility. It shows you files from folders on your computer and uses the standard Windows context menu for file operations. The app does not transmit, upload, sync, or share your files, folder contents, filenames, or file activity to any server.

---

## 1. What we collect

FanFolder sends one thing: an anonymous installation event, once, on the first successful launch for each user installation.

- **Anonymous Installation Identifier** — a 128-bit random hex string, generated on your device by a cryptographic random number generator. It is not derived from your account, machine name, Windows SID, or hardware serial. It is stored only on your device under `HKEY_CURRENT_USER\SOFTWARE\FanFolder` and is not tied to your name, email, Microsoft account, or any other personal information. It is not combined with any other data that could identify you.

- **App Version** — the version number in the FanFolder executable (for example, "1.2.2"). Read from the binary's file version resource.

- **CPU Architecture** — one of "x64", "arm64", "x86", or "unknown", determined at compile time.

- **Platform Identifier** — the fixed string "Windows".

- **Build Type** — a boolean "isDebug" flag, showing whether the build is debug or release.

- **Locale** — the fixed string "en-US" used by the telemetry payload; it is not read from your system locale settings.

---

## 2. What the network request reveals

The installation event goes to Aptabase as an HTTPS POST. Like any HTTPS request, Aptabase can see normal network metadata: your IP address and standard HTTP headers. Aptabase may use your IP to figure out a rough geographic region like country. FanFolder does not include your IP address or any network metadata in the event payload itself; Aptabase sees only what the HTTPS connection itself exposes.

---

## 3. What we do not collect

FanFolder does NOT collect, transmit, or store:

- filenames, folder paths, or any file content
- file activity (opens, renames, deletes, drag-and-drop)
- your name, email, Windows username, or Microsoft account
- your Windows product key, machine GUID, or hardware identifiers
- browsing history, clipboard, or keystrokes
- information about other applications on your device
- contacts, calendar, or account credentials
- any information about the files shown in the fan menu beyond what is needed to display them locally

The app reads the monitored folder to show its contents and reads the Windows Recent Documents list as a default source. Both are read-only and local; nothing is sent off the device.

---

## 4. How the installation event works

On the first successful launch after installation or update:

1. FanFolder checks `TelemetryFirstRunSent` in the registry. If it is already set, nothing is sent and the app continues normally.
2. If the flag is not set, FanFolder generates a random installation identifier (as described above) and stores it in the registry.
3. It sends a single HTTPS POST to `https://eu.aptabase.com/api/v0/events`. The request runs in a background thread using the Windows WinHTTP API, with a 3-second timeout for each stage. It does not block startup, and the app remains fully usable even without a network.
4. Only if the request succeeds (HTTP 2xx) does the app set `TelemetryFirstRunSent`. If it fails (no network, timeout, server error), the flag stays unset, and the app retries on a later launch.
5. On all later launches the flag is already set, so no further telemetry is sent for that installation.

---

## 5. About Aptabase

Aptabase is a product analytics service hosted in the European Union. It receives only the event payload described above and the network metadata from the HTTPS connection. Aptabase does not set tracking cookies and does not fingerprint your device. The developer uses the Aptabase dashboard only to count unique installations and to see the distribution of versions and CPU architectures.

Aptabase's privacy policy: <https://aptabase.com/legal/privacy>

---

## 6. Distribution channels

FanFolder is available through three channels. The privacy practices are the same regardless of how you get the app:

- **Direct download** from GitHub releases. GitHub logs download counts for each installer file; this is platform telemetry, not app telemetry. FanFolder does not send any data to GitHub.
- **winget package manager.** The winget manifest points to the same GitHub-hosted installer as the direct download. winget may collect its own usage telemetry as part of Windows; see the Microsoft Privacy Statement for details. FanFolder does not communicate with winget after installation.
- **Microsoft Store.** The Store records standard install and update counts as platform telemetry. FanFolder behaves identically across all three channels and does not send any additional data when installed from the Store.

---

## 7. Opting out

Telemetry is on by default but can be disabled at any time, even before the first launch. Once disabled, FanFolder will not generate, store, or send an installation identifier and will not contact Aptabase.

To opt out before launching FanFolder, run the following in PowerShell:

```powershell
New-Item -Path "HKCU:\SOFTWARE\FanFolder" -Force | Out-Null
Set-ItemProperty -Path "HKCU:\SOFTWARE\FanFolder" `
    -Name "TelemetryEnabled" -Type DWord -Value 0
```

To re-enable telemetry:

```powershell
Set-ItemProperty -Path "HKCU:\SOFTWARE\FanFolder" `
    -Name "TelemetryEnabled" -Type DWord -Value 1
```

If you disabled telemetry before the first launch, no installation event is ever sent. If you disabled it after the event was already sent, the random identifier stays in your registry but no further events are sent and no network call to Aptabase is made on subsequent launches.

---

## 8. Data storage

Everything FanFolder stores stays on your device under:

```
HKEY_CURRENT_USER\Software\FanFolder
```

This registry key holds application settings, the telemetry installation identifier (if telemetry is not disabled), and the "first run sent" flag. Uninstalling FanFolder removes the application files but does not automatically remove this registry key. To remove all FanFolder data, including the telemetry identifier, delete the registry key after uninstalling:

```powershell
Remove-Item -Path "HKCU:\SOFTWARE\FanFolder" -Recurse -Force
```

FanFolder does not store data in the cloud, in any online account, or anywhere outside this local registry key and the application's own installation directory.

---

## 9. Your rights

Because the only data FanFolder sends is an anonymous random identifier that is not linked to your name, account, or any other identifying information, the installation event is not personal data under most privacy regulations. Still, you have control:

- **Right to opt out:** Disable telemetry at any time as described above. No future events will be sent.
- **Right to remove stored data:** Delete the registry key as described above. This removes the installation identifier from your device.
- **Right to request deletion from the analytics service:** Because the identifier is random and not tied to you, it cannot be matched to an individual. If you wish, you may request that all FanFolder-related records be removed from the Aptabase dashboard by opening an issue on the project's GitHub repository and providing your installation identifier (which you can read from the registry using the path shown above before you delete it).

---

## 10. Changes to this notice

If FanFolder's data practices change in a material way, this notice will be updated and the "Last updated" date at the top will reflect the revision. If you are using an earlier version of the app, the practices described in the notice that accompanied that version apply. The current version of this notice is maintained at:

<https://github.com/olebhartvigsen/FanFolder/blob/main/PRIVACY.md>

---

## 11. Contact

Licensor: Ole Bülow Hartvigsen
Project:  FanFolder — <https://github.com/olebhartvigsen/FanFolder>

For questions about this privacy notice or FanFolder's data practices, please open an issue on the project's GitHub repository.
