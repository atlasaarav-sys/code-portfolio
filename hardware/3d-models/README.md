# CAD & 3D Models

SolidWorks mechanical design work — original assemblies and drawings, not
vendor/purchased-part files. Every `.SLDPRT`/`.SLDASM`/`.SLDDRW` file
requires SolidWorks (or a viewer that supports the format, e.g. the free
eDrawings viewer) to open.

## Projects

| Project | What it is |
|---|---|
| [differential-gear-box](differential-gear-box) | Full differential gearbox assembly — housing and four gears (20.1, 20.2, 40, 60 tooth) |
| [four-cylinder-engine](four-cylinder-engine) | Inline 4-cylinder engine assembly — piston, piston ring, piston pin, crankshaft, connecting rod + cap |
| [battle-bot](battle-bot) | Combat robot chassis part, wheel design (latest of several iterations), and a released drawing with dimensioned view + PDF |
| [portfolio-deck](portfolio-deck) | "Aarav Artham Portfolio SOLIDWORKS" slide deck — a curated walkthrough of SolidWorks design work, as both the original `.pptx` and a PDF export |

## differential-gear-box

- `DGBOX Assembly.SLDASM` — top-level assembly
- `G 20.1 DGBOX.SLDPRT`, `G 20.2 DGBOX.SLDPRT`, `G 40 DGBOX.SLDPRT`, `G 60 DGBOX.SLDPRT` — the four gears, named by tooth count

## four-cylinder-engine

- `4-CYL Engine.SLDASM` — top-level assembly
- `Piston 4-CYL.SLDPRT`, `Piston Ring 4-CYL.SLDPRT`, `Piston Pin 4-CYL.SLDPRT` — piston subassembly parts
- `Crankshaft 4-CYL.SLDPRT` — crankshaft
- `Connecting Rod 4-CYL.SLDPRT`, `Connecting rod cap 4-CYL.SLDPRT` — connecting rod + cap

## battle-bot

- `Part1.SLDPRT` — chassis/base part
- `Wheel.SLDPRT` — base wheel part
- `Wheel LH V4.SLDPRT` — final iteration of the left-hand wheel design (earlier V2/V3 iterations superseded and not included)
- `ME 302 Battle Bot Drawings/Wheel.SLDDRW` + `Wheel.pdf` — released drawing (dimensioned view) for the wheel, as both the native SolidWorks drawing and a PDF

## portfolio-deck

- `Aarav Artham Portfolio SOLIDWORKS.pptx` — original slide deck
- `Aarav Artham Portfolio SOLIDWORKS.pdf` — PDF export, previewable directly on GitHub
