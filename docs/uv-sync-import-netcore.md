# NETCORE-Paket mit uv installieren: `import netcore` funktioniert nicht

Kurze Anleitung zu einem häufigen Setup-Problem in diesem Repository.

## Was wir erreichen wollten

- Das Projekt **NETCORE** als normales Python-Paket `netcore` unter `src/netcore/` anlegen
- Mit `uv sync` Dependencies und das lokale Paket ins virtuelle Environment installieren
- Danach prüfen, ob alles stimmt:

  ```bash
  uv run python -c "import netcore; print(netcore.__version__)"
  ```

  Erwartung: Ausgabe `1.0.1`

`uv sync` meldet dabei oft erfolgreich:

```text
Installed 1 package
netcore==1.0.1 (from file:///.../NETCORE)
```

Trotzdem kann der Import fehlschlagen:

```text
ModuleNotFoundError: No module named 'netcore'
```

## Warum das passiert (editable install)

`uv sync` installiert das **eigene Projekt im Repo-Root standardmäßig als editable** (Entwicklungsmodus).

Dabei legt Hatchling typischerweise eine Datei wie `_editable_impl_netcore.pth` in `.venv/.../site-packages/` an, mit Inhalt etwa:

```text
/Users/.../NETCORE/src
```

Python liest `.pth`-Zeilen **ohne** `import ...` aber so, dass sie **relativ zu `site-packages`** interpretiert werden — nicht als absoluter Pfad. Der Eintrag nach `src/` landet deshalb **nicht** zuverlässig auf `sys.path`.

Folge:

- Metadaten sagen: Paket `netcore` ist installiert
- Modul `netcore` ist für Python trotzdem nicht importierbar

Das ist ein Problem des **editable-Installationswegs**, nicht davon, dass der Algorithmus noch in `NETCORE.py` liegt.

## Was stattdessen tun

Lokales Paket **ohne editable** installieren:

```bash
uv sync --group dev --no-editable
```

Danach erneut testen:

```bash
uv run python -c "import netcore; print(netcore.__version__)"
```

Optional prüfen, dass die Paketdateien wirklich im venv liegen:

```bash
ls .venv/lib/python3.12/site-packages/netcore/
```

Dort sollte u. a. `__init__.py` stehen (nicht nur eine `.pth`-Datei).

## Merksatz

| Befehl | Wirkung |
|--------|---------|
| `uv sync --group dev` | editable → `import netcore` kann fehlschlagen |
| `uv sync --group dev --no-editable` | Wheel-Inhalt in `site-packages` → `import netcore` funktioniert |

Für die weitere Entwicklung in diesem Repo: **`--no-editable` bei `uv sync` mitgeben**, bis editable installs hier zuverlässig funktionieren.

## Hinweis zum Projektstand

- `import netcore` → Paket-Skelett unter `src/netcore/` (Version, später Public API)
- Algorithmus (Legacy) → noch `NETCORE.py` im Repository-Root; Migration folgt im Refactor-Plan

Beides ist beabsichtigt und getrennt.
