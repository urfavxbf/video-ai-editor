import React from 'react';
import {AbsoluteFill, OffthreadVideo, Sequence, staticFile} from 'remotion';
import type {HyperFramesGraphic} from './validateHyperFramesGraphics';

/** Plays a locally rendered HyperFrames MP4 inside an approved episode.
 * Silent motion graphics only: the official Chatterbox narration remains the audio source.
 */
export const HyperFramesGraphicLayer: React.FC<{clip: HyperFramesGraphic}> = ({clip}) => {
  const full = clip.layout === 'fullscreen';
  return <Sequence from={clip.startFrame} durationInFrames={clip.durationFrames}>
    <AbsoluteFill style={{pointerEvents:'none'}}>
      <div style={full ? {
        position:'absolute',inset:0,overflow:'hidden',
      } : {
        position:'absolute',left:690,top:235,width:950,height:535,
        overflow:'hidden',borderRadius:28,border:'2px solid #69f9ba88',
        background:'#07111a',boxShadow:'0 24px 90px #06111d88',
      }}>
        <OffthreadVideo src={staticFile(clip.file)} muted
          style={{width:'100%',height:'100%',objectFit:'cover'}} />
      </div>
    </AbsoluteFill>
  </Sequence>;
};
