# Nerd Scroll Production Content Platform Plan

## Objective

Make Nerd Scroll a real installable Windows product, not a developer folder.

The product should let a normal user:

```text
1. Install Nerd Scroll.
2. Click a desktop icon.
3. Choose a starter pack, purchased pack, text file, book, Bible section, or theater scene.
4. Pick speed or display mode.
5. Start the show.
```

Nerd Scroll should become a content platform for cinematic text, terminal ambience, scrolling scenes, long-form reading, and ASCII theater.

---

## Definition of Done for v1.0

```text
[ ] Windows installer builds successfully.
[ ] Installer creates Start Menu shortcut.
[ ] Installer can create Desktop shortcut.
[ ] User does not need Python installed.
[ ] User sees simple folders only.
[ ] Three starter packs are included.
[ ] Purchased packs can be added easily.
[ ] User can paste their own text.
[ ] User can load text files.
[ ] Long text can be chunked for readable scrolling.
[ ] Theater Mode can play frame-based scenes.
[ ] Bible/book workflows are copyright-safe.
[ ] No pack text is executed.
[ ] All generated customer-facing folders use plain-English names.
```

---

## Human-Readable Installed Folder Model

Users should see simple names:

```text
Nerd Scroll
├── CLICK_TO_START_NERD_SCROLL.exe
├── README_FIRST.txt
├── PUT_TEXT_FILES_HERE
├── PUT_PURCHASED_PACKS_HERE
├── STARTER_PACKS_INCLUDED
└── ADVANCED_DO_NOT_EDIT
```

Internal files can live inside:

```text
ADVANCED_DO_NOT_EDIT
```

This keeps the installed product friendly while preserving the code structure needed by the app.

---

## Core Data Schema

### Pack metadata

```text
# title: Enterprise Mainframe Operations Vol. 1
# recommended_speed: normal
# category: mainframe ambience
# render_mode: scroll
# content_type: scene_pack
# creator: Nerd Scroll
# license: personal + streaming use, no resale
```

### Content library item

```json
{
  "id": "enterprise-mainframe-operations-vol-1",
  "title": "Enterprise Mainframe Operations Vol. 1",
  "file_path": "...",
  "content_type": "scene_pack",
  "render_mode": "scroll",
  "recommended_speed": "normal",
  "source_license": "premium pack",
  "safe_to_bundle": true
}
```

### Supported content types

```text
scene_pack
text_file
book
bible_section
theater_movie
mainframe_console
ambient_log
```

---

## Render Modes

### 1. Scroll Mode

Current behavior. Lines type or flood through a terminal window.

Best for:

```text
mainframe packs
logs
source code ambience
books
Bible reading
long text
```

### 2. Theater Mode

Frame-based animation. Frames are separated by markers:

```text
--- FRAME ---
```

Best for:

```text
ASCII movies
living maps
creature scenes
cyber city panoramas
portrait monitor scenes
```

### 3. Reading Mode

Text is chunked into readable blocks instead of raw endless lines.

Best for:

```text
books
Bible passages
public-domain stories
long documents
```

---

## Books Workflow

Users should be able to put a plain text book into:

```text
PUT_TEXT_FILES_HERE
```

Then Nerd Scroll should:

```text
1. Detect the text file.
2. Offer Reading Mode.
3. Chunk long paragraphs.
4. Add chapter/section dividers.
5. Let the user choose slow, normal, or bedtime speed.
6. Scroll forever or stop at the end.
```

Book safety rules:

```text
[ ] Use public-domain books.
[ ] Use user-owned writing.
[ ] Use properly licensed text.
[ ] Do not bundle modern copyrighted books without permission.
```

---

## Bible Workflow

Nerd Scroll can support Bible reading packs and scripture scrolling if the text source is license-safe.

Recommended Bible source for bundling:

```text
World English Bible, because it is dedicated to the public domain.
```

Bible modes:

```text
1. Chapter Scroll
2. Story Scroll
3. Verse-by-Verse Calm Mode
4. Portrait Scripture Theater
5. Daily Reading Pack
```

Bible quality rules:

```text
[ ] No altered scripture wording when presenting scripture.
[ ] Clearly identify translation/source.
[ ] Do not mix unrelated stories randomly.
[ ] Keep story chunks coherent.
[ ] Avoid overlapping/repeated passages unless intentional.
[ ] Keep black background / readable white or green text option.
```

---

## Mainframe Pack Direction

The mainframe pack lane should feel like a real operations window while staying fictional and safe.

Include realistic-looking areas:

```text
JCL
JES2 queue
SDSF-style display
COBOL compile listings
REXX/TSO helper scripts
IDCAMS / VSAM utility screens
SORT jobs
ABEND triage
DB2 batch output
CICS snapshots
MQ monitor output
End-of-window dashboard
```

Rules:

```text
[ ] No real company data.
[ ] No real hostnames or IPs.
[ ] No real credentials.
[ ] No claim of official IBM affiliation.
[ ] Keep datasets and users fictional.
```

---

## Pack Products

### Starter packs included with app

```text
Cyber City Starter
Mainframe Mystery Starter
Living Map Starter
```

### Paid packs

```text
Single pack: $0.99
10-pack bundle: $4.99
```

### Bundle ideas

```text
Mainframe Ops Bundle
Bible Reading Screens Bundle
Public Domain Classics Bundle
Living Maps Bundle
ASCII Theater Movies Bundle
Cozy Reading Terminal Bundle
Cyber City Theater Bundle
```

---

## Outside-the-Box Product Ideas

### Terminal Movies

Frame-based ASCII movies with optional portrait display.

### Living Books

Books that scroll with headers, chapter cards, ambient dividers, and optional visual motifs.

### Bible Story Packs

Scripture-preserving story sections that scroll cleanly from beginning to end.

### Ambient Desk Modes

Slow terminal scenes for stream backgrounds and desk setups.

### Creator Pack Builder

A future tool that asks:

```text
What theme do you want?
How long should it run?
Scroll or theater mode?
What speed?
```

Then it creates a pack template.

---

## Immediate Production Priority

Do not add major new features until the app can be installed cleanly.

Priority order:

```text
1. Build installable Windows package.
2. Simplify installed folder names.
3. Polish GUI copy.
4. Add Reading Mode.
5. Add Theater Mode.
6. Add Bible/book import workflow.
7. Build first premium pack bundle.
```
