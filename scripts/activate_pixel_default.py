"""Mark the exact 13 pose binaries ready only after real PNG and render verification.

This program does NOT claim original 3D rigging, natural mouth movements or audio sync.
"""
from pathlib import Path
import json
from stage_pixel_default_pack import verify_workspace

ROOT=Path(__file__).resolve().parents[1]
def activate(root=ROOT):
    n=verify_workspace(root)
    if n!=13: raise ValueError("Incomplete canonical PNG set")
    m_path=Path(root)/"characters/pixel-default-manifest.json"
    r_path=Path(root)/"characters/registry.json"
    m=json.loads(m_path.read_text(encoding="utf-8"))
    reg=json.loads(r_path.read_text(encoding="utf-8"))
    m["assetDelivery"]["assetsCommitted"]=True
    m["assetDelivery"]["assetReady"]=True
    m["assetDelivery"]["assetInstallation"]="all 13 original full-resolution PNG images verified in GitHub working tree"
    reg["character_hero_system"]["runtime_assets_ready"]=True
    reg["character_hero_system"]["next_art_step"]="Assets validated; integrate real English Chatterbox audio and align dialogue in long-form episodes."
    reg["default_video"]["visual_asset_status"]="13 owner-selected pixel PNG binaries present and SHA-256 verified; independent voice sync still episode-specific"
    reg["assets_location"]="public/characters/pixel-default/ (13 verified original images)"
    for who,rec in m["characters"].items():
        reg["characters"][who]["visual"]["pose_count"]=len(rec["poses"])
    m_path.write_text(json.dumps(m,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    r_path.write_text(json.dumps(reg,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("ACTIVATED: 13 verified PNGs; voice/caption synchronization not yet proved")
if __name__=="__main__":activate()
