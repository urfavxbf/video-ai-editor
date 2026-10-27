#!/usr/bin/env python3
"""Merge exactly 13 existing source skills into one portable CineForge Pro SKILL.md."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib
import posixpath
import re
import shutil

ROOT=Path(__file__).resolve().parent.parent
BASE=ROOT/".claude"/"skills"
DEST=BASE/"cineforge-pro"/"SKILL.md"
OUT=ROOT/"out"/"cineforge-pro"
PIN="30d4553ecd46fbc5212fd0ff006ae43af522158b"
OFFICIAL="https://github.com/remotion-dev/skills"
PROJECT="https://github.com/urfavxbf/video-ai-editor"
NAMES=[
 "ai-video-editor","remotion-best-practices","remotion-create",
 "remotion-markup","remotion-captions","remotion-studio","remotion-render",
 "remotion-interactivity","remotion-multimedia","remotion-maps",
 "remotion-docs","remotion-upgrade","remotion-saas"
]
LINKS=re.compile(r'(?<!!)\[([^\]\n]+)\]\(([^)\n]+)\)')
def merge_source(name):
    p=BASE/name/"SKILL.md"
    t=p.read_text(encoding="utf-8")
    m=re.match(r"\A---\n(.*?)\n---\n([\s\S]*)\Z",t,re.S)
    if not m or not re.search(r"^name:\s*"+re.escape(name)+r"\s*$",m.group(1),re.M):
        raise ValueError("Invalid source skill: "+name)
    body=m.group(2).strip()
    origin=(".claude/skills/"+name if name=="ai-video-editor" else "skills/"+name)
    root=(PROJECT+"/blob/main/" if name=="ai-video-editor"
          else OFFICIAL+"/blob/"+PIN+"/")
    def fix(x):
        label,url=x.group(1),x.group(2)
        if url.startswith(("https://","http://","#","mailto:","data:","/")) or " " in url:
            return x.group(0)
        namepart,sep,anchor=url.partition("#")
        path=posixpath.normpath(posixpath.join(origin,namepart))
        if path.startswith("../"):
            raise ValueError("Unsafe reference path: "+url)
        return "["+label+"]("+root+path+("#"+anchor if sep else "")+")"
    body=LINKS.sub(fix,body)
    lines=[]
    inside=None
    for line in body.splitlines():
        token=line.lstrip()[:3]
        if token in ("~~~",chr(96)*3):
            if inside is None: inside=token
            elif inside==token: inside=None
        if inside is None and re.match(r"^#{1,5}\s+",line):
            line="##"+line
        lines.append(line)
    return "\n".join(lines)

def main():
    pinfile=ROOT/"docs"/"REMOTION_SKILLS_SOURCE_COMMIT.txt"
    if pinfile.read_text(encoding="utf-8").strip()!=PIN:
        raise ValueError("Pinned Remotion skill revision changed")
    header="""---
name: cineforge-pro
description: All-in-one professional AI video creator and editor skill combining thirteen workflows. Use for podcast video editing, cinematic motion graphics, original Tagalog YouTube Shorts, Remotion animations, synchronized subtitles, audio, Studio previews, rendering and building a video editor.
---

# CINEFORGE PRO — AI Video Director & Motion Studio

ONE INSTALL • THIRTEEN MERGED SKILLS

The main instructions from the project's custom AI video editor and all 12
official Remotion Agent Skills are consolidated into this single SKILL.md.

## Operating principles

1. Identify whether the user wants a completed MP4, live preview, an
   editable composition, or a video-editing application. Honor prior output
   requirements and do not request details already supplied.
2. Verify user footage exists and inspect it before claiming editing decisions
   or describing its visuals. Use actual source timing and authentic dialogue.
3. Create professional, narrative-driven motion design. Favor expressive
   camera choices, purposeful reframing, tasteful kinetic captions, real
   emotional pacing and sound design over repetitive quote-card templates.
4. For original videos, write original scripts and use properly licensed
   visuals, voiceover and music. Independently verify time-sensitive or
   material scientific claims.
5. Prefer word-level timestamps. Proofread Tagalog/Taglish, place subtitles
   in safe areas, and disclose approximate timing when exact alignment fails.
6. Render deterministic Remotion animations from frames. Use appropriate
   Studio previews and real MP4 renders. Validate encoded duration, frames,
   video/audio streams, fonts, cropping, captions and sound.
7. A Skill provides guidance, not rendering hardware, npm packages, access
   to apps, permanent ChatGPT installation, or permissions. Never claim to
   have run a tool or rendered a video without supporting evidence.
8. Keep third-party notices intact. Never publish to YouTube automatically
   without user authorization or expose credentials and signed media URLs.
9. Follow the relevant module below for detailed implementation, while
   prioritizing the user's present task and the working host capabilities.

## Integrated modules

"""
    parts=[]
    for i,name in enumerate(NAMES,1):
        origin=(PROJECT+"/blob/main/.claude/skills/"+name+"/SKILL.md"
                if name=="ai-video-editor" else
                OFFICIAL+"/blob/"+PIN+"/skills/"+name+"/SKILL.md")
        parts.append("## Module "+str(i).zfill(2)+": "+name+
                     "\n\nSource: "+origin+"\n\n"+merge_source(name))
    footer="""
## Portability and provenance

Official Remotion Agent Skills: https://github.com/remotion-dev/skills
Pinned revision: 30d4553ecd46fbc5212fd0ff006ae43af522158b
Project custom skill: https://github.com/urfavxbf/video-ai-editor
Third-party notices: https://github.com/urfavxbf/video-ai-editor/blob/main/THIRD_PARTY_NOTICES.md

All 13 main SKILL.md contents are embedded here, so no additional Skill
installation is required. Some optional deep-reference materials are linked
to their exact official source version online instead of duplicated. They
are documentation, not separate Skills. Project-local commands require
an actual checkout of the associated project.

Remotion itself is a separately licensed framework. This compiled Skill
does not relicense upstream code or promise an executable runtime.

## Quality and delivery checklist

- Media and required output format actually verified.
- Authentic story beats, accurate language and subtitle timing.
- Effective motion graphics and appropriate audio balance.
- Proper source attribution and licensed assets.
- Actual rendered file checked for audio/video streams and playback.
- Only verified download links presented, never fabricated files.
"""
    final=header+"\n\n---\n\n".join(parts)+"\n\n"+footer
    if final.count("\n## Module ")!=13:
        raise RuntimeError("Wrong merged module count")
    DEST.parent.mkdir(parents=True,exist_ok=True)
    DEST.write_text(final,encoding="utf-8")
    OUT.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(DEST,OUT/"SKILL.md")
    zip_path=OUT/"CineForge-Pro-One-Skill.zip"
    with ZipFile(zip_path,"w",ZIP_DEFLATED,compresslevel=9) as z:
        z.write(DEST,"SKILL.md")
    with ZipFile(zip_path) as z:
        assert z.namelist()==["SKILL.md"] and z.testzip() is None
    print("COMPILED:",str(DEST))
    print("13 MODULES, length:",len(final))
    print("SHA256:",hashlib.sha256(final.encode()).hexdigest())
    print("ZIP:",str(zip_path))
    print("Ready for user installation, not installed in their ChatGPT account.")

if __name__=="__main__":
    main()
