# mk2conf Image Pipeline

Relevant when working on image handling in mkdocs2confluence (mk2conf).

## Pipeline stages

```
Markdown text
  -> parser/markdown.py  (_parse_inline_content)
  -> ImageNode(src, alt, title, width, height, align)
  -> transforms/images.py  (registers attachment, resolves attachment_name)
  -> emitter/xhtml.py  (_emit_image)
  -> <ac:image ac:align="..."> or bare <ac:image>
```

## Alignment — current behaviour (as of v0.13.12)

The parser sets `ImageNode.align` ONLY when the Markdown has an explicit attribute
block immediately after the closing parenthesis:

```
![alt](src){ align="center" }
```

A bare image on its own line:

```
![alt](src)
```

produces `align=None` → no `ac:align` attribute → Confluence defaults to left.

## Emitter

`_emit_image` in `emitter/xhtml.py` correctly emits `ac:align` when the field is set:

```python
align_attr = f' ac:align="{html.escape(node.align)}"' if node.align else ""
```

No change needed in the emitter. The gap is in the parser / a missing transform.

## Auto-centering lone-image paragraphs (not yet implemented)

Common MkDocs convention: a paragraph whose sole child is an `ImageNode` is treated as
a centred figure. To implement this:

1. Add a post-parse transform that walks `ParagraphNode` instances.
2. If the paragraph has exactly one child and it is an `ImageNode` with `align=None`,
   set `node.children[0].align = "center"`.
3. Place the transform before the images transform (which registers attachments) so
   attachment resolution is unaffected.

This is a deliberate design decision — opt-in vs auto-center — not an oversight.
The user should decide before implementation which they want as the default.
