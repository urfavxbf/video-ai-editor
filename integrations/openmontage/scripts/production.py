#!/usr/bin/env python3
"""Bounded local adapter. Codex, not this program, authors and approves stages."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys

INTEGRATION = Path(__file__).resolve().parents[1]
HOST = INTEGRATION.parents[1]
PIPELINE = 'documentary-montage'


def safe_path(base, relative):
    if not isinstance(relative, str) or not re.fullmatch(r'[A-Za-z0-9_./ -]+', relative):
        raise ValueError('Unsafe local path; URLs and special characters are not accepted')
    path = Path(relative)
    if path.is_absolute() or '..' in path.parts:
        raise ValueError('Path must remain inside its project')
    result = base / path
    if not result.resolve().is_relative_to(base.resolve()):
        raise ValueError('Path/symlink escapes project')
    return result


def number(value):
    if type(value) not in (int, float) or not math.isfinite(value):
        raise ValueError('Timing must be a finite number')
    return value


def read_json(path):
    def invalid(value):
        raise ValueError(f'Non-finite JSON value: {value}')
    return json.loads(path.read_text(), parse_constant=invalid)


def save_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')


def digest(path):
    checksum = hashlib.sha256()
    with path.open('rb') as source:
        for block in iter(lambda: source.read(1024 * 1024), b''):
            checksum.update(block)
    return checksum.hexdigest()


def probe_media(path):
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format',
                             '-of', 'json', str(path)], check=True, capture_output=True, text=True, timeout=30)
    return json.loads(result.stdout)


def validate_plan(data, *, fixture=False):
    brief, scene, manifest, edit = (data[k] for k in ('brief', 'scene_plan', 'asset_manifest', 'edit_decisions'))
    meta = brief['metadata']
    if meta.get('fixture', False) is not fixture or manifest['metadata'].get('fixture', False) is not fixture:
        raise ValueError('Fixture requires --fixture; production cannot use fixture artifacts')
    duration = number(brief['target_duration_seconds'])
    if not 2 <= duration <= 180 or brief['target_platform'] not in ('youtube', 'generic'):
        raise ValueError('First route supports 2–180 second landscape projects')
    if meta.get('language') != 'en' or meta.get('render_runtime') != 'remotion':
        raise ValueError('Approved English/Remotion runtime must be locked in brief')
    if edit.get('render_runtime') != 'remotion' or edit.get('renderer_family') != PIPELINE:
        raise ValueError('Documentary runtime lock requires Remotion')
    if meta.get('music_plan', {}).get('source') != 'none' or not meta.get('music_plan', {}).get('opt_out_reason'):
        raise ValueError('Music execution is not in this route; needs explicit approved opt-out or a follow-up adapter')
    if 'end_tag_plan' not in meta or meta['end_tag_plan'] is not None or not meta.get('end_tag_opt_out_reason'):
        raise ValueError('End-tag execution is not in this route; needs explicit approved opt-out or a follow-up adapter')
    for key in ('overlays', 'audio', 'music', 'transitions', 'end_tag', 'bespoke', 'composition_mode', 'subtitles'):
        if edit.get(key):
            raise ValueError(f'Unsupported first-route edit option: {key}')
    for key in ('grade_profile', 'silence_window', 'l_cuts', 'compose_target'):
        if key in edit.get('metadata', {}):
            raise ValueError(f'Unsupported first-route metadata: {key}')
    cuts, scenes = edit['cuts'], scene['scenes']
    if not 1 <= len(cuts) <= 60 or len(scenes) != len(cuts):
        raise ValueError('Need 1–60 corresponding motion cuts/scenes')
    cursor, seen = 0.0, set()
    for cut, shot in zip(cuts, scenes):
        start, end = number(cut['in_seconds']), number(cut['out_seconds'])
        if start < 0 or end <= start or cut.get('speed', 1) != 1 or cut.get('transform') or cut.get('layer', 'primary') != 'primary' or 'backgroundColor' in cut:
            raise ValueError('Invalid cut bounds or unsupported transform/speed/layer')
        if any(cut.get(k, 'cut') != 'cut' for k in ('transition_in', 'transition_out')) or cut.get('transition_duration', 0) != 0:
            raise ValueError('First route accepts hard cuts only')
        if cut['source'] in seen or shot['type'] != 'broll' or shot['id'] != cut['id']:
            raise ValueError('Need unique motion asset per matching broll scene')
        seen.add(cut['source'])
        if abs(number(shot['start_seconds']) - cursor) > 0.001 or abs(number(shot['end_seconds']) - cursor - end + start) > 0.001:
            raise ValueError('Scene and edit timing disagree')
        cursor += end - start
    if abs(cursor - duration) > 0.001:
        raise ValueError('Brief and edit duration disagree')
    narration = manifest['metadata']['narration']
    registry = read_json(HOST / 'characters/registry.json')
    character = registry['characters'].get(narration.get('character'))
    wanted = 'fixture-tone-not-speech' if fixture else (character or {}).get('english_voice', {}).get('identifier')
    if not character or narration.get('voice_id') != wanted or narration.get('language') != 'en':
        raise ValueError('Approved English Chatterbox voice identity required; no provider substitutions')
    if not narration.get('alignment_review'):
        raise ValueError('Actual WAV word-alignment review is required')
    last, words = 0.0, []
    for segment in narration['segments']:
        for word in segment['words']:
            start, end = number(word['start']), number(word['end'])
            if not isinstance(word['word'], str) or not word['word'].strip() or start < last or end <= start or end > duration:
                raise ValueError('Invalid or overlapping caption word timing')
            last = end
            words.append(word)
    if not words:
        raise ValueError('Reviewed caption words are required')
    return duration


def gate_context(stages, current, checkpoints):
    context = {}
    for stage in stages:
        if stage['name'] == current:
            break
        cp = checkpoints.get(stage['name']) or {}
        if cp.get('status') != 'completed' or cp.get('pipeline_type') != PIPELINE or (stage.get('human_approval_default') and cp.get('human_approved') is not True):
            raise ValueError(f"Awaiting owner approval: {stage['name']}")
        content = json.dumps(cp['artifacts'], sort_keys=True, separators=(',', ':'), allow_nan=False)
        context[stage['name']] = hashlib.sha256(content.encode()).hexdigest()
    return context


def require_approvals(stages, checkpoints, data):
    for stage in stages:
        if stage['name'] == 'compose':
            break
        cp = checkpoints.get(stage['name']) or {}
        if cp.get('status') != 'completed' or cp.get('pipeline_type') != PIPELINE or (stage.get('human_approval_default') and cp.get('human_approved') is not True):
            raise ValueError(f"Awaiting owner approval: {stage['name']}")
        for name in stage['produces']:
            if cp.get('artifacts', {}).get(name) != data[name]:
                raise ValueError(f'Artifact changed after approval: {name}; review and checkpoint again')
        if cp.get('metadata', {}).get('prerequisites', {}) != gate_context(stages, stage['name'], checkpoints):
            raise ValueError(f"Changed prerequisite approval: {stage['name']}; review and checkpoint again")


def validate_media(project, data, *, fixture=False, probe=probe_media):
    duration = validate_plan(data, fixture=fixture)
    manifest = data['asset_manifest']
    provenance, narration = (manifest['metadata'][k] for k in ('provenance', 'narration'))
    assets, paths, probes = {}, {}, {}
    for asset in manifest['assets']:
        asset_id = asset['id']
        if asset_id in assets or asset['type'] not in ('video', 'narration'):
            raise ValueError('Duplicate asset or unsupported media type')
        if asset.get('cost_usd') != 0 or not all(asset.get(k) for k in ('provider', 'original_url', 'license')):
            raise ValueError(f'Missing zero-cost provenance/license: {asset_id}')
        if (asset['provider'] == 'lavfi-fixture') is not fixture:
            raise ValueError('Generated fixture media cannot be used as production footage/narration')
        path = safe_path(project, asset['path'])
        evidence = provenance.get(asset_id, {})
        if not evidence.get('rights_review') or not evidence.get('reviewed_by'):
            raise ValueError(f'Missing rights review: {asset_id}')
        if not path.is_file() or digest(path) != evidence.get('sha256'):
            raise ValueError(f'Media missing or hash changed: {asset_id}')
        assets[asset_id], paths[asset_id], probes[asset_id] = asset, path, probe(path)
    for cut in data['edit_decisions']['cuts']:
        asset = assets.get(cut['source'], {})
        info = probes.get(cut['source'], {})
        if asset.get('type') != 'video' or asset.get('scene_id') != cut['id'] or not any(s['codec_type'] == 'video' for s in info.get('streams', [])):
            raise ValueError('Cut must reference real matching motion footage')
        if cut['out_seconds'] > float(info['format']['duration']) + 0.001:
            raise ValueError('Cut extends beyond actual footage')
    voice = narration['asset_id']
    if assets.get(voice, {}).get('type') != 'narration' or paths[voice].suffix.lower() != '.wav':
        raise ValueError('Approved narration WAV missing')
    if provenance[voice]['sha256'] != narration['audio_sha256']:
        raise ValueError('Caption alignment WAV hash mismatch')
    if not any(s['codec_type'] == 'audio' for s in probes[voice]['streams']) or abs(float(probes[voice]['format']['duration']) - duration) > 0.05:
        raise ValueError('Actual narration WAV duration must match the edit (within 50 ms)')
    if any(w['end'] > float(probes[voice]['format']['duration']) for s in narration['segments'] for w in s['words']):
        raise ValueError('Caption exceeds actual audio duration')
    return paths


def load_runtime():
    runtime = safe_path(INTEGRATION, '.runtime/openmontage')
    pin = (INTEGRATION / 'UPSTREAM_COMMIT').read_text().strip()
    if not (runtime / '.git').is_dir():
        raise ValueError('Not installed. Run bash integrations/openmontage/scripts/setup.sh --skip-tts')
    actual = subprocess.check_output(['git', '-C', str(runtime), 'rev-parse', 'HEAD'], text=True).strip()
    dirty = subprocess.check_output(['git', '-C', str(runtime), 'status', '--porcelain', '--untracked-files=no'], text=True).strip()
    if actual != pin or dirty:
        raise ValueError('Upstream SHA mismatch or modified tracked source; restore reviewed checkout first')
    python = runtime / '.venv/bin/python'
    if not python.is_file():
        raise ValueError('Missing isolated Python. Run setup.sh --skip-tts')
    if Path(sys.prefix) != runtime / '.venv':
        os.execv(str(python), [str(python), str(Path(__file__).resolve()), *sys.argv[1:]])
    sys.path.insert(0, str(runtime))
    os.chdir(runtime)
    # Use upstream's default projects root; do not let inherited overrides escape isolation.
    os.environ.pop('OPENMONTAGE_PROJECTS_DIR', None)
    return runtime


def project_path(runtime, slug):
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug) or len(slug) > 80:
        raise ValueError('Project ID must be a short kebab-case slug')
    project = safe_path(runtime, f'projects/{slug}')
    for name in ('artifacts', 'assets', 'renders', 'history'):
        safe_path(project, name)
    # Covers upstream's marker/checkpoint .tmp and history archive leaf writes,
    # including dangling symlinks which Path.exists() would miss.
    if project.is_symlink() or (project.exists() and any(p.is_symlink() for p in project.rglob('*'))):
        raise ValueError('Project symlink is forbidden, including checkpoint temporary/history files')
    return project


def transport_edit(canonical, paths, narration, subtitle, duration):
    edit = copy.deepcopy(canonical)
    for cut in edit['cuts']:
        cut['source'] = str(paths[cut['source']].resolve())
        # Pinned upstream omits zero fade frames when these fields are absent.
        cut['transition_in'] = cut['transition_out'] = 'cut'
    words = [w for s in narration['segments'] for w in s['words']]
    edit['captions'] = {'words': [{'word': w['word'], 'startMs': w['start'] * 1000, 'endMs': w['end'] * 1000} for w in words],
                        'wordsPerPage': 4, 'fontSize': 54, 'highlightColor': '#22D3EE'}
    edit['subtitles'] = {'enabled': True, 'source': str(subtitle)}
    edit.setdefault('metadata', {})['proposal_render_runtime'] = 'remotion'
    edit['metadata']['target_duration_seconds'] = duration
    return edit


def review_checkpoint_status(result):
    if result.get('operation') != 'remotion_render':
        raise ValueError('Runtime evidence is not a Remotion render; no downgrade accepted')
    status = result.get('final_review', {}).get('status')
    if status == 'pass':
        return 'completed'
    if status == 'revise':
        return 'awaiting_human'
    raise ValueError('Missing or failed final QA review')


def preflight(runtime, registry, manifest):
    from lib.pipeline_loader import get_stage_order
    voice = subprocess.run([sys.executable, str(HOST / 'scripts/check_chatterbox_v3.py')], capture_output=True, text=True, timeout=30)
    tools = {name: registry.get(name).get_info()['status'] for name in ('video_compose', 'direct_clip_search', 'clip_search', 'subtitle_gen')}
    return {'upstream_commit': (INTEGRATION / 'UPSTREAM_COMMIT').read_text().strip(),
            'agent': 'Current Codex session; no second agent needed', 'pipeline': PIPELINE,
            'stages': get_stage_order(manifest), 'tools': tools,
            'runtime': 'Remotion required; FFmpeg for mux/probe; no HyperFrames substitution',
            'narration': {'ready': voice.returncode == 0, 'check': (voice.stdout + voice.stderr).strip(),
                          'note': 'Loader check only, not inference. Approved existing WAV can be used without model installation.'},
            'footage': 'Not downloaded/proven by preflight. Supply reviewed local clips or inspect real search errors.',
            'status': 'degraded' if voice.returncode else 'preflight-only', 'paid_calls': 0}


def render_project(project, manifest, registry, *, fixture=False):
    from lib.checkpoint import read_checkpoint, write_checkpoint, validate_checkpoint
    from schemas.artifacts import validate_artifact
    names = [name for stage in manifest['stages'] if stage['name'] != 'compose' for name in stage['produces']]
    data = {name: read_json(safe_path(project, f'artifacts/{name}.json')) for name in names}
    for name, value in data.items():
        validate_artifact(name, value)
    checkpoints = {s['name']: read_checkpoint(project.parent, project.name, s['name']) for s in manifest['stages']}
    for stage, cp in checkpoints.items():
        if cp:
            validate_checkpoint(cp)
            if cp['stage'] != stage or cp['project_id'] != project.name:
                raise ValueError('Checkpoint identity mismatch')
    require_approvals(manifest['stages'], checkpoints, data)
    paths = validate_media(project, data, fixture=fixture)
    duration = validate_plan(data, fixture=fixture)
    renders = safe_path(project, 'renders')
    output = safe_path(project, f"renders/{'fixture' if fixture else 'final'}.mp4")
    if output.exists():
        raise ValueError('Output exists; use a new project ID for a new reviewed render')
    # Ensure all tool-created destinations remain inside this run, including hidden review/temp paths.
    if renders.exists() and any(p.is_symlink() for p in renders.rglob('*')):
        raise ValueError('Symlink found in render destination')
    compose = registry.get('video_compose')
    if not compose.get_info().get('render_engines', {}).get('remotion'):
        raise ValueError('Remotion is unavailable; runtime downgrade is forbidden')
    narration = data['asset_manifest']['metadata']['narration']
    words = [w for s in narration['segments'] for w in s['words']]
    write_checkpoint(project.parent, project.name, 'compose', 'in_progress', {}, pipeline_type=PIPELINE)
    subtitle = safe_path(project, 'assets/captions.srt')
    result = registry.get('subtitle_gen').execute({'segments': narration['segments'], 'format': 'srt', 'output_path': str(subtitle)})
    if not result.success:
        raise ValueError('Subtitle tool failed: ' + str(result.error))
    edit = transport_edit(data['edit_decisions'], paths, narration, subtitle, duration)
    result = compose.execute({'operation': 'render', 'edit_decisions': edit,
        'asset_manifest': data['asset_manifest'], 'scene_plan': data['scene_plan']['scenes'],
        'audio_path': str(paths[narration['asset_id']].resolve()), 'output_path': str(output),
        'script_text': ' '.join(w['word'] for w in words), 'remotion_timeout_ms': 120000})
    if not result.success:
        save_json(safe_path(project, 'artifacts/render_failure.json'), {'fixture': fixture, 'error': result.error, 'data': result.data})
        raise ValueError('Pinned render failed; see artifacts/render_failure.json; no fallback attempted')
    info = probe_media(output)
    video = next(s for s in info['streams'] if s['codec_type'] == 'video')
    audio = next(s for s in info['streams'] if s['codec_type'] == 'audio')
    if (video['codec_name'], video['width'], video['height'], video['r_frame_rate'], audio['codec_name']) != ('h264', 1920, 1080, '30/1', 'aac') or abs(float(info['format']['duration']) - duration) > 0.1:
        raise ValueError('Encoded output failed canvas/fps/codec/duration QA')
    subprocess.run(['ffmpeg', '-v', 'error', '-i', str(output), '-f', 'null', '-'], check=True, timeout=180)
    for index, at in enumerate((0.1, duration / 4, duration / 2, duration - 0.1)):
        subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(at), '-i', str(output), '-frames:v', '1', '-y',
                        str(safe_path(project, f'renders/qa-{index}.jpg'))], check=True, timeout=30)
    final_review = result.data['final_review']
    save_json(safe_path(project, 'artifacts/final_review.json'), final_review)
    checkpoint_status = review_checkpoint_status(result.data)
    report = {'version': '1.0', 'outputs': [{'path': str(output.relative_to(project)), 'format': 'mp4',
        'codec': 'h264', 'audio_codec': 'aac', 'resolution': '1920x1080', 'fps': 30,
        'duration_seconds': float(info['format']['duration']), 'file_size_bytes': output.stat().st_size}],
        'warnings': ['Fixture only: generated motion and tone, NOT speech or a finished episode'] if fixture else ['Technical QA only; owner audiovisual review is still required'],
        'verification_notes': ['Pinned registry video_compose Remotion render, approved WAV mux, cinematic word captions; full decode passed'],
        'render_grammar': PIPELINE, 'metadata': {'fixture': fixture, 'upstream_commit': (INTEGRATION / 'UPSTREAM_COMMIT').read_text().strip(),
        'paid_calls': 0, 'review_status': final_review['status'], 'checkpoint_status': checkpoint_status,
        'caption_words': len(words), 'music_opt_out': data['brief']['metadata']['music_plan']['opt_out_reason'],
        'end_tag_opt_out': data['brief']['metadata']['end_tag_opt_out_reason']}}
    validate_artifact('render_report', report)
    validate_artifact('final_review', final_review)
    save_json(safe_path(project, 'artifacts/render_report.json'), report)
    save_json(safe_path(project, 'artifacts/final_review.json'), final_review)
    save_json(safe_path(project, 'artifacts/ffprobe.json'), info)
    write_checkpoint(project.parent, project.name, 'compose', checkpoint_status, {'render_report': report, 'final_review': final_review}, pipeline_type=PIPELINE)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('preflight')
    init = commands.add_parser('init')
    init.add_argument('project')
    init.add_argument('--title', required=True)
    gate = commands.add_parser('checkpoint')
    gate.add_argument('project')
    gate.add_argument('stage', choices=('idea', 'scene_plan', 'assets', 'edit'))
    gate.add_argument('--approve', help='Record an actual owner decision reference, never infer approval')
    render = commands.add_parser('render')
    render.add_argument('project')
    render.add_argument('--fixture', action='store_true')
    args = parser.parse_args()
    try:
        runtime = load_runtime()
        from lib.pipeline_loader import load_pipeline
        from lib.checkpoint import init_project, read_checkpoint, write_checkpoint
        from tools.tool_registry import registry
        manifest = load_pipeline(PIPELINE)
        if args.command == 'preflight':
            registry.discover()
            print(json.dumps(preflight(runtime, registry, manifest), indent=2))
            return 0
        project = project_path(runtime, args.project)
        if args.command == 'init':
            if project.exists():
                raise ValueError('Project already exists; preserve it and use another ID')
            init_project(args.project, title=args.title, pipeline_type=PIPELINE)
            print(project)
        elif args.command == 'checkpoint':
            stage = next(s for s in manifest['stages'] if s['name'] == args.stage)
            predecessors = manifest['stages'][:manifest['stages'].index(stage)]
            prior_checkpoints = {s['name']: read_checkpoint(project.parent, project.name, s['name']) for s in predecessors}
            prior_data = {n: read_json(safe_path(project, f'artifacts/{n}.json')) for s in predecessors for n in s['produces']}
            require_approvals(predecessors, prior_checkpoints, prior_data)
            context = gate_context(manifest['stages'], args.stage, prior_checkpoints)
            artifacts = {n: read_json(safe_path(project, f'artifacts/{n}.json')) for n in stage['produces']}
            if args.approve:
                previous = read_checkpoint(project.parent, project.name, args.stage)
                if not args.approve.strip() or not previous or previous['status'] != 'awaiting_human' or previous['artifacts'] != artifacts or previous.get('metadata', {}).get('prerequisites', {}) != context:
                    raise ValueError('Approval requires an identical awaiting_human artifact and owner decision reference')
            write_checkpoint(project.parent, project.name, args.stage,
                'completed' if args.approve else 'awaiting_human', artifacts, pipeline_type=PIPELINE,
                human_approved=bool(args.approve), metadata={'owner_decision_reference': args.approve, 'prerequisites': context})
            print('Recorded owner approval' if args.approve else 'Awaiting owner approval; do not advance')
        else:
            registry.discover()
            print(json.dumps(render_project(project, manifest, registry, fixture=args.fixture), indent=2))
        return 0
    except (ValueError, KeyError, OSError, subprocess.SubprocessError) as exc:
        print(f'BLOCKED: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
