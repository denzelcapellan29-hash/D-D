# Approved asset-generation and visual-QA workflow (2026-10-09)

Status: DM-APPROVED. Scope: Acquisitions Incorporated Episode 1 Area 2; reusable for future individual 3D assets. Area 2 remains the sole active visual benchmark. This replaces older assumptions that Blender is the primary modeling tool or that Foundry/3D Canvas is required for asset QA.

## Canonical workflow
1. Read official source and semantic asset requirements; distinguish source-grounded facts from artistic interpretation. Prepare one isolated, unambiguous image reference using ChatGPT image generation (NOT Meshy's built-in text-to-image). Show the image to the DM and obtain approval before credit-bearing 3D generation.
2. Upload the exact approved PNG to private Google Drive staging, preserving original bytes and versioned filename.
3. Use Google Drive fetch(download_raw_file=true, include_base64=false) to obtain a short-lived signed raw-file download_url. Immediately pass that URL to Meshy image-to-3D (image_url); do not pass Drive preview/share URLs, ChatGPT sandbox paths, or assume Meshy's server can read ChatGPT files. The signed URL expires; fetch anew per job. Keep signed URLs and tokens out of GitHub/logs. This handoff was successfully verified with task 01a12364-e7c4-77dc-9c2a-26b25bb99110.
4. Generate in Meshy 7.1 standard with textures/PBR, 2K texture and GLB output (adjust settings only by explicit asset requirement). Check task status; record task ID, credits, and source image identity.
5. Download GLB and textures to the existing Drive-synced asset directory. Do not overwrite a released asset. The successful basin GLB was saved at G:\My Drive\D&D\Foundry Bridge\assets\Area2_StoneBasin_ChatGPT_Meshy71_v001.glb.
6. Use Blender ONLY as a standalone renderer/visual QA stage. Do not use Blender to author, remodel, or alter the Meshy asset unless the DM explicitly requests it. Do not involve Foundry/3D Canvas in this asset-only review stage.
7. Isolate the newly imported GLB from any pre-existing Blender scene objects; validate model-only bounds, mesh count, textures and camera framing. Render actual GLB at three-quarter, opposite, front, side, overhead, plus close-ups where needed. Never present source concept art or unrelated scene renders as GLB QA. Inspect actual renders before issuing a QA verdict.
8. Save QA images in the Drive-synced captures folder; verify their presence in Google Drive, link the folder for DM review, and document defects, geometry/material concerns, and acceptance status. User approval gates any additional production or proceeding beyond Area 2.

## Proven successful checkpoint
Asset: Area2 Stone Basin, Meshy task 01a12364-e7c4-77dc-9c2a-26b25bb99110, 30 credits, GLB ~39,901,356 bytes. Reference staging: https://drive.google.com/file/d/13a7YNKYa9dHtv1xUUL3tQxzHmrnOeyUQ/view . Five actual Blender-rendered QA views: https://drive.google.com/drive/folders/1kZn3smwPwGPMUjqNbIzQE-A9JTOlvU_N . DM verdict: 'visually stunning'; this is the dedicated workflow.

## Operational safeguards
- Execute the full routine autonomously rather than requiring separate prompts for each phase.
- Meshy access has standing user consent; platform-generated authorization prompts cannot be overridden by assistant.
- Meshy generation costs credits: obtain specific approval for new credit-bearing jobs where the integration requires it; approval for a prior job does not automatically approve unlimited spending.
- Fail fast: stop on unexpected handoff/capture failures; one targeted retry at most.
- Source PDF/private adventure material stays in Drive, not GitHub. GitHub stores only workflow instructions, manifests, and code.
- Do not claim an artifact is reviewed until genuine renders have been inspected. Do not claim ChatGPT Project UI instructions have been edited without a supported direct UI tool.
