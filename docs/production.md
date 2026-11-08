# NOVAWORLD: THE LOST KINGDOM — production plan

## Logline
Two young sky-island explorers, Mira and Tavi, discover that the Heart Crystal keeping their floating homeland in balance is fading. Their journey through the Luminous Wilds teaches them that the world can only be restored through cooperation.

## Main cast
- **Mira** — curious, brave, observant; carries a sun-thread scarf.
- **Tavi** — inventive, funny, loyal; builds small gliders from fallen skywood.
- **The Echo Keeper** — a mysterious guardian who communicates through light and sound.

## Twelve-chapter structure (about five minutes each)
1. The Sky Islands — introduce NovaWorld and the explorers.
2. A Fading Light — the Heart Crystal begins to dim.
3. Map of the Wind — the friends find an ancient sky map.
4. The Luminous Wilds — they cross a glowing forest.
5. The River Above — a floating river reveals a hidden passage.
6. The Echo Keeper — a guardian tests their patience and trust.
7. The Shattered Bridge — they solve a teamwork challenge.
8. The City in the Clouds — they learn the history of the crystal.
9. The Storm Gate — a great storm separates the friends.
10. Two Paths, One Promise — they reunite and make a plan.
11. The Heart of NovaWorld — they restore the crystal through cooperation.
12. A New Dawn — the islands bloom and a new adventure is hinted at.

## Rendering reality
A full hour of 24 fps animation is 86,400 frames. The included Blender scene generator is a technical starting point, not a finished hour-long movie: it creates a reusable stylized environment and animated character placeholders. Each chapter still needs authored action, dialogue, voice acting, music, camera coverage, and final quality review. Free GitHub runners are suitable for short tests and chapter-sized low-resolution jobs, but cannot guarantee a complete 60-minute high-quality render within free limits.

## Suggested workflow
1. Render a 10–20 second test.
2. Review character design, camera framing, lighting, and output.
3. Build chapter-specific scenes and dialogue.
4. Render each chapter as an individual MP4.
5. Join completed chapters with FFmpeg using a concat list.
