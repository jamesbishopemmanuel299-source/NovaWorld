# NOVAWORLD: THE LOST KINGDOM

A procedural 3D cartoon film project built with Blender Python and FFmpeg.

## Film plan
- Target runtime: 60 minutes
- Structure: 12 chapters, approximately 5 minutes each
- Genre: original 3D fantasy adventure
- Characters and world are original; this project is not affiliated with Avatar or any existing franchise.

## Rendering approach
Render one chapter at a time. GitHub Actions can produce low-resolution test renders, but a full 60-minute high-quality render may exceed free runner time and storage limits. The workflow is manual so you can render chapters individually and assemble them locally or in a later cloud job.

## Requirements
- Blender 4.x
- FFmpeg
- Python 3

## Local preview
```bash
blender -b -P blender/create_film.py -- --chapter 1 --frames 300 --output renders/chapter_01.mp4
```

The default short preview is intentionally much shorter than the final chapter. Increase `--frames` for longer renders. See `docs/production.md` for the chapter plan and safe render settings.
