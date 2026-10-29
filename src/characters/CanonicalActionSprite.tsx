import React from 'react';
import {Img, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';

export type CanonicalAction = 'idle'|'explain'|'wave'|'point'|'walk'|'celebrate'|'listen';
export type CanonicalCharacter = 'urfavxbf'|'pix';
export const CANONICAL_ACTIONS: CanonicalAction[] = ['idle','explain','wave','point','walk','celebrate','listen'];

export type CanonicalActionSpriteProps = {
  character: CanonicalCharacter;
  action: CanonicalAction;
  width: number;
  height: number;
  assetsReady: boolean;
  artApproved?: boolean;
  /** Drafts may be previewed only in explicitly labelled review compositions. */
  reviewDraft?: boolean;
  startFrame?: number;
  playbackFps?: number;
};

/** Reusable source-art 2.5D full-body motion playback. No legacy V2 fallback. */
export const CanonicalActionSprite: React.FC<CanonicalActionSpriteProps> = ({
  character,action,width,height,assetsReady,artApproved=false,reviewDraft=false,
  startFrame=0,playbackFps=12,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  if(!CANONICAL_ACTIONS.includes(action))throw new Error('Unknown canonical full-body action');
  if(!Number.isFinite(playbackFps)||playbackFps<1||playbackFps>60)throw new Error('Invalid sprite playback fps');
  const index = Math.floor(Math.max(0,frame-startFrame)*playbackFps/fps)%8;
  const filename = `characters/canonical/${character}/actions/${action}/${String(index).padStart(3,'0')}.png`;
  const display = assetsReady && (reviewDraft || artApproved);
  return <div data-canonical-character={character} data-action={action}
    data-art-status={artApproved?'approved':reviewDraft?'draft-review':'blocked'}
    style={{width,height,position:'relative',flexShrink:0,pointerEvents:'none'}}>
    {display ? <Img src={staticFile(filename)} style={{
      width:'100%',height:'100%',objectFit:'contain',imageRendering:'auto',
    }}/> : <div style={{
      display:'flex',flexDirection:'column',alignItems:'center',justifyContent:'center',
      width:'100%',height:'100%',border:'2px dashed #467c78',borderRadius:16,
      color:'#bce9e4',background:'#0d2028',fontFamily:'monospace',fontSize:21,textAlign:'center'
    }}>CANONICAL FULL-BODY ART PENDING
      <span style={{marginTop:16,fontSize:16}}>{character} / {action} — no fallback</span>
    </div>}
    {display && !artApproved && <div style={{
      position:'absolute',left:0,right:0,bottom:0,textAlign:'center',
      padding:7,color:'#e4f4ff',background:'rgba(14,24,38,.86)',
      fontFamily:'monospace',fontSize:13
    }}>DRAFT 2.5D ART • NOT PRODUCTION APPROVED</div>}
  </div>;
};
