#!/usr/bin/env python3
"""Stage-0 OpenMontage integration using the actual pinned upstream Python modules.

Deliberately does not load previous character assets, media, or episode code.
"""
from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
EPISODE = REPO / "openmontage" / "episodes" / "youtube-beginners-journey"
UPSTREAM = Path(os.environ.get("OPENMONTAGE_ROOT", REPO / ".openmontage")).resolve()
PROJECT_ID = "youtube-beginners-journey"

if not (UPSTREAM / "pipeline_defs" / "animated-explainer.yaml").is_file():
    raise SystemExit("OpenMontage upstream checkout is required: set OPENMONTAGE_ROOT.")
sys.path.insert(0, str(UPSTREAM))

# These are the real OpenMontage modules, NOT stand-in JSON validation.
from lib.checkpoint import init_project, write_checkpoint  # noqa: E402
from lib.pipeline_loader import get_stage_order, load_pipeline_readonly  # noqa: E402
from schemas.artifacts import validate_artifact  # noqa: E402


def read(name: str) -> dict:
    with (EPISODE / name).open(encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    research = read("research_brief.json")
    proposal = read("proposal_packet.json")
    manifest = load_pipeline_readonly("animated-explainer")
    stages = get_stage_order(manifest)
    assert stages[:2] == ["research", "proposal"], stages
    validate_artifact("research_brief", research)
    validate_artifact("proposal_packet", proposal)

    if len(research["data_points"]) < 3 or len(research["sources"]) < 5:
        raise ValueError("Research is below the upstream minimum evidence requirement.")
    if len(research["angles_discovered"]) < 3:
        raise ValueError("Research requires at least three grounded angles.")
    if proposal["approval"]["status"] != "pending":
        raise ValueError("This bootstrap must not manufacture human approval.")
    if proposal["cost_estimate"]["total_estimated_usd"] != 0:
        raise ValueError("External paid generation is prohibited.")
    if proposal["cost_estimate"]["budget_cap_usd"] != 0:
        raise ValueError("This episode has an explicit zero-USD budget cap.")
    if any(item.get("estimated_usd", 0) > 0
           for item in proposal["cost_estimate"]["line_items"]):
        raise ValueError("Paid asset or render actions are not authorized.")
    if not research["metadata"].get("fresh_assets_only"):
        raise ValueError("Fresh-asset policy is not enabled.")
    if not proposal["metadata"].get("fresh_assets_only"):
        raise ValueError("Fresh-asset policy missing from proposal.")

    # Only a new project workspace; cannot access any previous repo media.
    root = Path(os.environ.get("OPENMONTAGE_PROJECTS_DIR", str(UPSTREAM / "projects"))).resolve()
    project = init_project(
        PROJECT_ID,
        title="YouTube Beginner's Journey — Fresh Start",
        pipeline_type="animated-explainer",
        pipeline_dir=root,
    )
    for directory in ("images", "video", "audio", "music"):
        if any((project / "assets" / directory).rglob("*")):
            raise ValueError(f"Existing media in fresh project assets/{directory}.")

    artifacts = project / "artifacts"
    artifacts.mkdir(exist_ok=True, parents=True)
    for name in ("research_brief.json", "proposal_packet.json"):
        shutil.copyfile(EPISODE / name, artifacts / name)

    research_cp = write_checkpoint(
        root, PROJECT_ID, "research", "completed", {"research_brief": research},
        pipeline_type="animated-explainer",
        cost_snapshot={"total_spent_usd": 0, "total_reserved_usd": 0, "budget_remaining_usd": 0},
        review={"research_sources": len(research["sources"]), "status": "schema_validated"},
    )
    proposal_cp = write_checkpoint(
        root, PROJECT_ID, "proposal", "awaiting_human", {"proposal_packet": proposal},
        pipeline_type="animated-explainer",
        human_approval_required=True, human_approved=False,
        cost_snapshot={"total_spent_usd": 0, "total_reserved_usd": 0, "budget_remaining_usd": 0},
        review={"status": "schema_validated_and_pending_approval"},
    )
    print(f"Validated upstream pipeline: {manifest['name']}; stages: {stages}")
    print(f"Research completed: {research_cp}")
    print(f"Proposal awaiting approval: {proposal_cp}")
    print(f"Fresh assets present: 0; paid services authorized: 0; video rendered: NO")


if __name__ == "__main__":
    main()
