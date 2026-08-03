FanFolder Privacy Notice

Copyright (c) 2026 Ole Bülow Hartvigsen. All rights reserved.

Last updated: 31 July 2026

This Privacy Notice explains how FanFolder ("the App") handles
information when the App is installed on Your device, whether You
obtain the App through a direct download, the winget package
manager, or the Microsoft Store. By installing and using the App,
You acknowledge the practices described in this Notice.

──────────────────────────────────────────────────────────────────────
1. OVERVIEW — FANFOLDER IS DESIGNED TO BE PRIVATE
──────────────────────────────────────────────────────────────────────

FanFolder is a local Windows taskbar utility. The App displays files
from folders on Your computer and shells out to the standard Windows
context menu for file operations. FanFolder does not transmit, upload,
sync, or otherwise share Your files, folder contents, filenames, or
file activity to any server at any time.

All of Your file data remains on Your local device unless You
explicitly open, move, or share it through Windows or another
application of Your choosing — none of this is handled or routed
through FanFolder.

──────────────────────────────────────────────────────────────────────
2. INFORMATION COLLECTED
──────────────────────────────────────────────────────────────────────

FanFolder collects one piece of information: an anonymous
installation event, sent once on first successful launch per
per-user installation.

  (a) Anonymous Installation Identifier — a 128-bit random hex
      string, generated locally using a cryptographic random number
      generator. The identifier is:
        - generated on Your device, not derived from any account,
          machine name, Windows SID, or hardware serial;
        - stored only on Your device under
          HKEY_CURRENT_USER\SOFTWARE\FanFolder;
        - not tied to Your name, email, Microsoft account, or any
          other personally identifiable information;
        - not combined with any other data source that could
          re-identify You.

  (b) App Version — the version number embedded in the FanFolder
      executable (for example, "1.2.2"). Read from the binary's file
      version resource.

  (c) CPU Architecture — one of "x64", "arm64", "x86", or
      "unknown", determined at compile time.

  (d) Platform Identifier — the fixed string "Windows".

  (e) Build Type — a boolean "isDebug" flag indicating whether the
      build is a debug or release configuration.

  (f) Locale — the fixed string "en-US" used by the telemetry
      payload; it is not read from Your system locale settings.

──────────────────────────────────────────────────────────────────────
3. INFORMATION DERIVED FROM THE NETWORK REQUEST
──────────────────────────────────────────────────────────────────────

The installation event is sent as an HTTPS POST request to the
Aptabase analytics service (see Section 5). Like any HTTPS request,
the receiving service — Aptabase — may observe network-level
metadata associated with the connection, including Your IP address
and standard HTTP request headers. Aptabase may derive coarse
geographic region (such as country) from this IP address for
aggregate analytics. FanFolder does not include Your IP address or
any network metadata in the event payload itself; what Aptabase
receives is limited to what the HTTPS transport exposes.

──────────────────────────────────────────────────────────────────────
4. INFORMATION FANFOLDER DOES NOT COLLECT
──────────────────────────────────────────────────────────────────────

FanFolder does NOT collect, transmit, or store:

  - filenames, folder paths, or any file content;
  - file activity (opens, renames, deletes, drag-and-drop actions);
  - Your name, email, Windows username, or Microsoft account;
  - Your Windows product key, machine GUID, or hardware identifiers;
  - browsing history, clipboard contents, or keystrokes;
  - information about other applications on Your device;
  - contacts, calendar, or account credentials;
  - any information about files shown in the fan menu other than
    what is needed to display them locally.

The App reads the monitored folder to display its contents on screen
and reads the Windows Recent Documents list as one of its default
folder sources. Both of these are read-only operations performed
locally; their contents are never transmitted off the device.

──────────────────────────────────────────────────────────────────────
5. HOW THE INSTALLATION EVENT WORKS
──────────────────────────────────────────────────────────────────────

On first successful launch of the App after installation or update:

  (a) FanFolder checks a registry flag (TelemetryFirstRunSent). If the
      flag is already set, no event is sent and the App continues
      normally.

  (b) If the flag is not set, the App generates a random installation
      identifier (Section 2a) and stores it in the registry.

  (c) The App sends a single HTTPS POST request to:
          https://eu.aptabase.com/api/v0/events
      The request is made in a background thread using the Windows
      WinHTTP API, with a 3-second connection and send timeout on each
      stage. The request never blocks application startup, and
      FanFolder remains fully usable even if the network is
      unavailable or the request fails.

  (d) Only if the request succeeds (HTTP 2xx response) does the App
      set the "TelemetryFirstRunSent" flag. If the request fails for
      any reason — no network, timeout, server error — the flag is
      not set, and the request is retried on a later launch.

  (e) On all subsequent launches, the flag is already set, so no
      further telemetry is sent for that installation.

──────────────────────────────────────────────────────────────────────
6. THE APTABASE SERVICE
──────────────────────────────────────────────────────────────────────

The installation event is processed by Aptabase, a privacy-focused
product analytics service hosted in the European Union. Aptabase
receives only the event payload described in Section 2 and the
network-level metadata described in Section 3. Aptabase does not set
tracking cookies and does not fingerprint Your device. FanFolder's
developer uses the Aptabase dashboard solely to count unique
installations of the App and to see the distribution of versions and
CPU architectures in use.

Aptabase's privacy policy is available at:
    https://aptabase.com/legal/privacy

──────────────────────────────────────────────────────────────────────
7. DISTRIBUTION CHANNELS
──────────────────────────────────────────────────────────────────────

FanFolder is distributed through three channels, and the same
privacy practices apply regardless of how You obtained the App:

  (a) Direct download from the project's GitHub releases. GitHub
      logs standard download counts for each installer file; this is
      platform telemetry, not app telemetry. FanFolder does not send
      any data to GitHub.

  (b) The winget package manager. The winget manifest points to the
      same GitHub-hosted installer as direct download. winget may
      collect its own usage telemetry as part of Windows; see the
      Microsoft Privacy Statement for details. FanFolder does not
      communicate with winget after installation.

  (c) The Microsoft Store. The Store records standard install and
      update counts as platform telemetry. FanFolder itself behaves
      identically across all three channels and does not send any
      additional data when installed from the Store.

──────────────────────────────────────────────────────────────────────
8. OPTING OUT
──────────────────────────────────────────────────────────────────────

Telemetry is on by default but can be disabled at any time, including
before the first launch of the App. Once disabled, FanFolder will not
generate, store, or send an installation identifier and will not
contact Aptabase.

To opt out before launching FanFolder, run the following in
PowerShell:

    New-Item -Path "HKCU:\SOFTWARE\FanFolder" -Force | Out-Null
    Set-ItemProperty -Path "HKCU:\SOFTWARE\FanFolder" `
        -Name "TelemetryEnabled" -Type DWord -Value 0

To re-enable telemetry:

    Set-ItemProperty -Path "HKCU:\SOFTWARE\FanFolder" `
        -Name "TelemetryEnabled" -Type DWord -Value 1

If You disabled telemetry before the first launch, no installation
event is ever sent. If You disable telemetry after the event was
already sent, the random identifier remains stored in Your registry
but no further events will be sent and no network call to Aptabase
will be made on subsequent launches.

──────────────────────────────────────────────────────────────────────
9. DATA STORAGE
──────────────────────────────────────────────────────────────────────

All data that FanFolder stores is kept on Your local device under:

    HKEY_CURRENT_USER\Software\FanFolder

This registry key holds the application's configuration settings, the
telemetry installation identifier (if telemetry has not been
disabled), and the "first run sent" flag. Uninstalling FanFolder
removes the application files but does not automatically remove this
registry key. To remove all FanFolder data, including the telemetry
identifier, delete the registry key after uninstalling:

    Remove-Item -Path "HKCU:\SOFTWARE\FanFolder" -Recurse -Force

FanFolder does not store any data in the cloud, in any online
account, or in any location other than this local registry key and
the application's own installation directory.

──────────────────────────────────────────────────────────────────────
10. CHILDREN
──────────────────────────────────────────────────────────────────────

FanFolder is a general-purpose file utility and is not directed at
children. The App does not knowingly collect any information from
children or from any other user beyond the anonymous installation
event described in this Notice. If You believe a child has provided
information to us through the App, and the App has not sent any
personally identifiable data, contact us so the installation record
can be removed from the Aptabase dashboard.

──────────────────────────────────────────────────────────────────────
11. YOUR RIGHTS
──────────────────────────────────────────────────────────────────────

Because the only data FanFolder sends is an anonymous random
identifier that is not linked to Your name, account, or any other
identifying information, the installation event is not personal data
under most privacy regulations. Nonetheless, You have control:

  - Right to opt out: Disable telemetry at any time as described in
    Section 8. No future events will be sent.
  - Right to remove stored data: Delete the registry key as described
    in Section 9. This removes the installation identifier from Your
    device.
  - Right to request deletion from the analytics service: Because the
    identifier is random and not tied to You, it cannot be matched to
    an individual. If You wish, You may request that all FanFolder-
    related records be removed from the Aptabase dashboard by writing
    to the contact address in Section 13 and providing Your
    installation identifier (which You can read from the registry
    using the path shown in Section 9 before You delete it).

──────────────────────────────────────────────────────────────────────
12. CHANGES TO THIS NOTICE
──────────────────────────────────────────────────────────────────────

If FanFolder's data practices change in a material way, this Notice
will be updated and the "Last updated" date at the top will reflect
the revision. If You are using an earlier version of the App, the
practices described in the Notice that accompanied that version
apply. The current version of this Notice is maintained at:

    https://github.com/olebhartvigsen/FanFolder/blob/main/PRIVACY.md

──────────────────────────────────────────────────────────────────────
13. CONTACT
──────────────────────────────────────────────────────────────────────

Licensor: Ole Bülow Hartvigsen
Project:  FanFolder — https://github.com/olebhartvigsen/FanFolder

For questions about this Privacy Notice or FanFolder's data
practices, please open an issue on the project's GitHub repository.
