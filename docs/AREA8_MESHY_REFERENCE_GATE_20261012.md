# Area 8 Meshy reference decision (2026-10-12)

DM explicitly chose **the most reliable integrated workflow**, not the cheapest image generator: retain Meshy text-to-image for references, inspect the actual reference, then Meshy 7.1 standard textured GLB and Blender geometry QA. Meshy reference costs 3–9 credits; no controlled evidence that ChatGPT image generation produces superior GLB structure. Do NOT silently switch to ChatGPT generation just to avoid the reference fee.

Installed AI 3D Asset Workflow **v2.6.2**, release `pluginrel_6acd35a44e888191a3c76b734407f81c`, readback verified. Binding skill ref `MESHY_REFERENCE_AND_ANNULAR_SILHOUETTE_V262.md` specifies hard pre-3D reference silhouette gate and technical dimensions held separately in JSON.

Area8 history: radial v016 generated an overly broad horseshoe, rejected; v017 technical 30-degree image generated a GLB appearing pie-shaped, without a preserved concave inner annulus opening, rejected. The next reference must show a single physical cut 30-degree annular slab, concave inner boundary and clear negative space, clean three-quarter perspective, no dimension arrows or text on the 3D input. Inspect image before spending GLB credits; inspect actual GLB afterward. Preserve v014 floor/wall/corner DM accepted *visual* baseline. v017 is saved experimental, not approved. Kenney/Quaternius only construction learning.
