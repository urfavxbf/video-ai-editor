#!/usr/bin/env python3
"""Stage original Blue App visuals into the ignored pinned OpenMontage checkout."""
from __future__ import annotations
import argparse
from pathlib import Path

SRC_ANCHOR='import { Composition, CalculateMetadataFunction } from "remotion";'
ROOT_ANCHOR="    </>\n  );\n};"
MARKER='id="BlueAppVisual"'

def stage(integration: Path, composer: Path) -> None:
    root_file = composer / "src" / "Root.tsx"
    component=integration/"creative"/"BlueAppVisual.tsx"
    if not root_file.is_file() or not (composer/"package.json").is_file():
        raise RuntimeError("Expected pinned OpenMontage Remotion composer")
    if not component.is_file():
        raise RuntimeError("Original Blue App visual component is missing")
    text=root_file.read_text(encoding="utf-8")
    if MARKER not in text:
        if text.count(SRC_ANCHOR)!=1 or text.count(ROOT_ANCHOR)!=1:
            raise RuntimeError("Upstream Root.tsx changed; refusing unsafe automatic patch")
        text=text.replace(SRC_ANCHOR,SRC_ANCHOR+'\nimport { BlueAppVisual } from "./BlueAppVisual";',1)
        composition='''      <Composition
        id="BlueAppVisual"
        component={BlueAppVisual}
        fps={30}
        width={1920}
        height={1080}
        durationInFrames={2070}
        defaultProps={{cuts: [], captions: [], audio: {}}}
        calculateMetadata={({props}) => ({
          durationInFrames: Math.max(30, Math.ceil(
            ((props.cuts?.length ? props.cuts[props.cuts.length - 1].out_seconds : 69) + 1) * 30
          ))
        })}
      />
'''
        text=text.replace(ROOT_ANCHOR,composition+ROOT_ANCHOR,1)
        root_file.write_text(text,encoding="utf-8")
    dest=composer/"src"/"BlueAppVisual.tsx"
    dest.write_text(component.read_text(encoding="utf-8"),encoding="utf-8")
    assert MARKER in root_file.read_text(encoding="utf-8")
    print("Staged original BlueAppVisual in pinned OpenMontage Remotion")

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--integration",type=Path,required=True)
    parser.add_argument("--composer",type=Path,required=True)
    args=parser.parse_args()
    stage(args.integration,args.composer)
