---
name: extract-pdf-text-on-macos-with-pypdf
description: Extract text from a local PDF on macOS when native Spotlight metadata is insufficient, using python3 and pypdf.
version: "1.0"
tags: [pdf, text-extraction, macos, python, pypdf]
tool_agnostic: true
authors: [Anders Hybertz]
tested_on: []
---

# Extract PDF text on macOS with pypdf

Use this when a user provides a local PDF path and you need readable text in the CLI.

## When to use
- Local PDF exists on disk
- `mdls` shows page count but `kMDItemTextContent` is null or incomplete
- `pdftotext` is not installed

## Steps
1. Verify the file exists and note its size:
   - `python3 - <<'PY'`
   - Use `Path(...).exists()` and `stat().st_size`
2. Check available extraction options:
   - `shutil.which('pdftotext')`
   - try importing `pypdf`
3. If `pypdf` is missing, install it for the current user:
   - `python3 -m pip install --user pypdf`
4. Extract text page by page with `PdfReader` and write a sidecar text file next to the PDF or in Downloads.
5. Read the extracted `.txt` file in chunks for analysis.

## Example extraction script
```python
from pathlib import Path
from pypdf import PdfReader
p = Path('/path/to/file.pdf')
reader = PdfReader(str(p))
out = p.with_suffix('.txt')
chunks = []
for i, page in enumerate(reader.pages, start=1):
    text = page.extract_text() or ''
    chunks.append(f'\n\n=== PAGE {i} ===\n\n{text}')
out.write_text(''.join(chunks))
print(out)
```

## Verification
- Confirm page count from `PdfReader`
- Confirm output file path exists
- Read the output text and inspect for truncation or OCR issues

## Pitfalls
- Scanned PDFs may need OCR; `pypdf` only extracts embedded text layers
- Extracted text may contain odd glyph substitutions or line breaks
- Large PDFs should be read in chunks
