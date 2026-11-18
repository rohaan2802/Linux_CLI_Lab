# Verification record

## Executed checks

The saved Ubuntu/WSL demo completed 24 exercises with zero command failures. It verified the ten input fixtures against their SHA-256 manifest, tested five mode-400 filenames including a leading-dash operand, reconstructed 16 wordlist entries, checked a 37-byte local transfer and compared a hex round-trip byte for byte.

Eight regression tests passed in Linux and Windows. They cover decimal addition, invalid/non-finite inputs, fixture path traversal, valid file lists, atomic evidence replacement and the supplied leading-dash filename.

## Scope

The demo runs in a temporary workspace and uses a loopback HTTP server. Root sessions, apt changes, locate index administration and host SSH service changes are documented VM reference tasks. Their current privileged execution is outside the saved demo evidence.

The banking model describes proposed controls. It does not claim a deployed banking application or an operational security certification. Saved exercise durations describe one run.

## Reproduce

    python3 -m cli_lab demo
    python3 -m unittest discover -s tests -v
    python tools/build_showcase.py
    python tools/verify_showcase.py

## Presentation checks

The static site passed Edge checks at 320, 390, 768, 1280 and 1440 pixels in both light and dark themes. The checks exercised the mobile menu and active section, dataset filtering, empty gallery searches, category filters, image zoom, Previous/Next, keyboard navigation, swipe handling and Back to Top.

All 24 full images are 1440 x 900. Their matching previews are 960 x 600. Gallery paths and order match the README. All local HTML and README resources were verified.

The rebuilt PDF has 61 pages. Its last 24 pages preserve the original submission. Page text, dimensions and rendered content were compared with the original. The command-line wheel built and its fixture installation was verified in a temporary environment.



The evidence CLI passed a fresh 24-exercise Linux run and eight regression checks, including missing/tampered steps and invalid timings. The README, site and PDF use the v2 enlarged figure set.

Navbar links were compared with the page section order. Each link's landing and active highlight passed at 320, 390, 768, 1280 and 1440 pixels in both themes, including the Files and Author boundaries. The source builder and presentation verifier enforce the same section order.

Eight expanded project chapters are sourced from data/project_sections.json and included in the README, static site, project handbook and rebuilt PDF. Their presence is checked by the presentation verifier.

Latest content verification: the 24 figure pairs, local resource paths, shared chapter coverage and original PDF appendix checks passed. A fresh regression run passed six checks; two temporary-file checks were blocked by Windows folder permissions in this session. The latest expanded layout could not receive a fresh browser run because automatic approval review was unavailable. Earlier responsive checks remain recorded above.
