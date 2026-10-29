#!/usr/bin/env python3
"""OFFLINE (zero-credit) programmatic whole-frame vector drawing studies.
Every frame is freshly rasterized from a different pose geometry, not formed
by cutting apart or transforming an original character image.
Art is newly drawn in a reference-inspired simplified style; NOT final owner art.
"""
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import json,math,hashlib,zipfile,io,os

OUT=Path(os.environ.get('ZERO_BUDGET_OUT','out/zero-budget-frame-studies')).resolve()
ROOT=OUT/'source-frames'
SIZE=512
S=2
C={
 'ink':'#10191c','hair':'#151c1c','hair2':'#202725','green':'#69f882','forest':'#0e4437',
 'forest2':'#155b45','muted':'#24624b','shirt':'#171c20','skin':'#ffd1ae','blush':'#f3ac9a',
 'pants':'#222528','shoe':'#1b272a','cyan':'#75edff','cyan2':'#31c9ff',
 'purple':'#9261e8','pink':'#ff91d0','snow':'#e3f7ff','skyshade':'#b5d8fc'
}
SPEC={
 'urfavxbf':{'idle':6,'talk':8,'point_camera':8,'point_object':8,'explain':8,'walk':12,'run':10,'jump':8,'laugh':8,'think':6,'surprised':6,'confused':6,'wave':8,'celebrate':8,'listen':6},
 'pix':{'idle':6,'talk':8,'assist_point':8,'walk':12,'run':10,'jump':8,'laugh':8,'curious':6,'surprised':6,'confused':6,'wave':8,'celebrate':8,'listen':6,'happy_bounce':8,'sleepy':6}
}
class Art:
    def __init__(self):
        self.im=Image.new('RGBA',(SIZE*S,SIZE*S),(0,0,0,0));self.d=ImageDraw.Draw(self.im)
    def box(self,b,fill,outline=None,width=2,r=0):
        b=tuple(int(v*S) for v in b)
        self.d.rounded_rectangle(b,radius=int(r*S),fill=fill,outline=outline,width=int(width*S))
    def ellipse(self,b,fill,outline=None,width=2):
        self.d.ellipse(tuple(int(v*S) for v in b),fill=fill,outline=outline,width=max(1,int(width*S)))
    def poly(self,pts,fill,outline=None,width=2):
        a=[(int(x*S),int(y*S)) for x,y in pts];self.d.polygon(a,fill=fill)
        if outline:self.d.line(a+[a[0]],fill=outline,width=int(width*S),joint='curve')
    def stroke(self,pts,fill,width=4,joint='curve'):
        self.d.line([(int(x*S),int(y*S)) for x,y in pts],fill=fill,width=int(width*S),joint=joint)
    def save(self,path):
        self.im.resize((SIZE,SIZE),Image.Resampling.LANCZOS).save(path,optimize=True)

def line_limb(a,start,end,w,c,inner,hand=False):
    # The complete limb is painted afresh at this specific frame geometry.
    elbow=((start[0]+end[0])/2,(start[1]+end[1])/2+abs(end[0]-start[0])*.05)
    a.stroke([start,elbow,end],C['ink'],w+7)
    a.stroke([start,elbow,end],c,w)
    a.stroke([start,(start[0]*.65+elbow[0]*.35,start[1]*.65+elbow[1]*.35)],inner,max(3,w//3))
    if hand:
        a.ellipse((end[0]-13,end[1]-11,end[0]+13,end[1]+12),C['skin'],C['ink'],2)
        for i in range(3):
            a.stroke([(end[0]-8+i*8,end[1]+1),(end[0]-8+i*8,end[1]+8)],C['blush'],1.2)

def action_pose(action,i,n,who):
    t=i/n*math.tau;s=math.sin(t);c=math.cos(t)
    q={'bounce':2*math.sin(t),'headtilt':0,'l_eye':'open','r_eye':'open',
       'mouth':'smile','left':(155,320),'right':(358,320),'handsize':1,
       'footL':(227,440),'footR':(287,440),'bodyX':0,'bodyY':0,'jump':0,'turn':0}
    if action in ('idle','listen'):
        q['bounce']=2*s; q['headtilt']=1.2*s
        if i==n-1:q['l_eye']=q['r_eye']='blink'
    if action in ('talk','explain'):
        q['mouth']=['small','wide','round','smile','small','wide','smile','round'][i%8]
        q['left']=(140+6*s,274+13*c);q['right']=(372-10*s,276+14*s)
        q['bounce']=2*s
    if action in ('point_camera','assist_point'):
        q['right']=(275+18*s,222+13*c);q['left']=(164,317)
        q['mouth']='wide' if i in (3,4,5) else 'smile'; q['handsize']=1.7
        q['headtilt']=1.5*s
    if action=='point_object':
        q['right']=(425+7*s,251+6*c);q['left']=(161,314)
        q['mouth']='small';q['turn']=4
    if action=='walk':
        q['footL']=(227+38*s,434-12*max(0,c));q['footR']=(287-38*s,434-12*max(0,-c))
        q['left']=(155-20*s,307);q['right']=(358+20*s,307);q['bounce']=5*abs(s)
        q['headtilt']=1.4*s
    if action=='run':
        q['footL']=(227+58*s,421-22*max(0,c));q['footR']=(287-58*s,421-22*max(0,-c))
        q['left']=(196-30*s,270+18*c);q['right']=(316+30*s,270-18*c)
        q['bounce']=9*abs(s);q['mouth']='wide'
    if action=='jump':
        h=[0,8,35,61,65,41,14,0][round(i*7/max(1,n-1))];q['jump']=-h
        q['left']=(162,240-h*.2);q['right']=(350,240-h*.2)
        q['footL']=(227,426-18*math.sin(math.pi*i/(n-1)))
        q['footR']=(287,426-18*math.sin(math.pi*i/(n-1)))
        q['mouth']='wide'
    if action=='laugh':
        q['left']=(205+7*s,307);q['right']=(308-7*s,306)
        q['mouth']='wide';q['l_eye']=q['r_eye']='happy';q['headtilt']=4*s
        q['bounce']=5*abs(s)
    if action in ('think','curious'):
        q['right']=(295+6*s,243);q['left']=(153,327)
        q['headtilt']=3+s*2;q['mouth']='small'
    if action=='surprised':
        q['left']=(160-15*s,254);q['right']=(353+15*s,254)
        q['mouth']='round';q['bounce']=3*abs(s)
    if action=='confused':
        q['headtilt']=6*s;q['right']=(334,244+8*c);q['mouth']='small'
    if action=='wave':
        q['right']=(353+19*s,155+12*c);q['left']=(154,315)
        q['headtilt']=2*s;q['mouth']='smile'
    if action=='celebrate':
        q['left']=(173+9*s,164-12*abs(c));q['right']=(345-9*s,164-12*abs(c))
        q['mouth']='wide';q['bounce']=9*abs(s)
        q['footL']=(212-5*s,437);q['footR']=(302+5*s,437)
    if action=='happy_bounce':
        q['jump']=-18*abs(s);q['mouth']='wide';q['l_eye']=q['r_eye']='happy'
    if action=='sleepy':
        q['bounce']=-2*abs(s);q['headtilt']=4+1*s
        q['l_eye']=q['r_eye']='happy';q['mouth']='small'
    # Multi-harmonic secondary wrist movement makes a full new drawn gesture
    # for each action cell; unlike whole-image shifts this modifies articulation.
    q['left']=(q['left'][0] + 3*math.cos(t+0.41),q['left'][1]+4*math.sin(t+0.79))
    q['right']=(q['right'][0] + 3*math.sin(t+0.28),q['right'][1]+4*math.cos(t+0.37))
    q['headtilt']+=2.4*math.sin(t+0.16)+1.1*math.cos(2*t+0.53)
    return q

def host(a,q,action,i):
    X=lambda n:n+q['bodyX']; Y=lambda n:n+q['bodyY']+q['bounce']+q['jump']
    ink=C['ink'];
    # Layer-order: feet and legs are freshly redrawn polygons based on ankle geometry.
    for hip,ankle in (((228,367),q['footL']),((285,367),q['footR'])):
        end=(ankle[0],ankle[1])
        a.poly([(X(hip[0]-21),Y(hip[1]-3)),(X(hip[0]+20),Y(hip[1]-3)),
                (X(end[0]+21),Y(end[1]-11)),(X(end[0]-18),Y(end[1]-11))],C['pants'],ink,4)
        a.stroke([(X(hip[0]-9),Y(hip[1]+3)),(X(end[0]-8),Y(end[1]-25))],C['green'],5)
        a.box((X(end[0]-29),Y(end[1]-9),X(end[0]+32),Y(end[1]+19)),C['shoe'],ink,4,9)
        a.box((X(end[0]-30),Y(end[1]+11),X(end[0]+35),Y(end[1]+21)),'#eaf7ec',ink,2,4)
        a.stroke([(X(end[0]-5),Y(end[1])),(X(end[0]+14),Y(end[1]))],C['green'],3)
    # torso and hood
    a.ellipse((X(184),Y(269),X(325),Y(363)),'#1a392d',ink,4)
    a.poly([(X(191),Y(285)),(X(207),Y(260)),(X(300),Y(260)),(X(321),Y(285)),
            (X(318),Y(375)),(X(193),Y(375))],C['forest'],ink,5)
    a.poly([(X(221),Y(281)),(X(287),Y(281)),(X(297),Y(367)),(X(216),Y(367))],C['shirt'],ink,3)
    # X shirt
    a.stroke([(X(240),Y(315)),(X(265),Y(340))],C['green'],8)
    a.stroke([(X(266),Y(315)),(X(239),Y(339))],C['green'],8)
    for off in (0,1):
        a.stroke([(X(209+off*92),Y(279)),(X(205+off*99),Y(357))],C['green'],4)
    a.stroke([(X(201),Y(366)),(X(309),Y(366))],C['green'],6)
    # arms fully redrawn per keyframe
    for side,end in [('left',q['left']),('right',q['right'])]:
        start=(201 if side=='left' else 314,285)
        end=(X(end[0]),Y(end[1]))
        line_limb(a,(X(start[0]),Y(start[1])),end,28,C['forest2'],C['green'],hand=True)
        a.ellipse((end[0]-9,end[1]-6,end[0]+9,end[1]+9),C['skin'],ink,1)
    if action in ('point_camera','point_object'):
        v=q['right'];cx=X(v[0]);cy=Y(v[1]);r=14*q['handsize'];
        a.ellipse((cx-r,cy-r,cx+r,cy+r),C['skin'],ink,3)
        if action=='point_object':a.stroke([(cx,cy),(cx+25,cy-7)],C['skin'],10)
        else:a.ellipse((cx-5,cy-10,cx+9,cy+4),'#ffddae',ink,2)
    # neck / head. Whole head and face details drawn afresh with expression params.
    a.box((X(239),Y(252),X(272),Y(283)),C['skin'],ink,3,10)
    tilt=q['headtilt'];cx=X(257)+tilt;cy=Y(197)
    a.ellipse((cx-94,cy-95,cx+94,cy+92),C['skin'],ink,5)
    a.ellipse((cx-86,cy+22,cx-65,cy+43),C['blush'])
    a.ellipse((cx+66,cy+21,cx+88,cy+42),C['blush'])
    # large green eyes / expressive eyelids
    for dx,eye in [(-42,q['l_eye']),(41,q['r_eye'])]:
        ex=cx+dx;ey=cy+11
        if eye=='open':
            a.ellipse((ex-24,ey-18,ex+24,ey+19),'white',ink,4)
            a.ellipse((ex-14,ey-15,ex+12,ey+16),'#38b75c',ink,2)
            a.ellipse((ex-7,ey-11,ex+8,ey+12),'#123922')
            a.ellipse((ex-8,ey-10,ex-1,ey-3),'white')
        elif eye=='happy':
            a.stroke([(ex-19,ey+4),(ex,ey-9),(ex+18,ey+5)],ink,5)
        else:a.stroke([(ex-19,ey),(ex+19,ey)],ink,5)
    mouth=q['mouth']
    if mouth=='wide':a.ellipse((cx-19,cy+45,cx+19,cy+65),'#6f273b',ink,3)
    elif mouth=='round':a.ellipse((cx-10,cy+45,cx+10,cy+68),'#6f273b',ink,3)
    elif mouth=='small':a.ellipse((cx-11,cy+48,cx+10,cy+57),'#833d42',ink,2)
    else:a.stroke([(cx-17,cy+49),(cx,cy+56),(cx+17,cy+49)],'#833e47',3)
    # tousled black-green hair spikes with unique accents
    spikes=[]
    for k in range(15):
        ang=math.pi*1.07+ k*(math.pi*.85/14)
        r=103+(8 if k%2 else 24)
        spikes.append((cx+math.cos(ang)*r,cy+math.sin(ang)*r))
    hairpts=[(cx-92,cy-33),(cx-105,cy-73)]+spikes+[(cx+103,cy-53),(cx+89,cy+5),(cx+60,cy-46),(cx+27,cy-29),(cx+9,cy-66),(cx-26,cy-29),(cx-64,cy-41)]
    a.poly(hairpts,C['hair'],ink,4)
    for k in range(8):
        xx=cx-86+k*22
        yy=cy-70-(k%3)*7
        a.stroke([(xx,yy),(xx+12,yy-24),(xx+34,yy-23)],C['hair2'],6)
        if k%2==0:a.stroke([(xx+6,yy-14),(xx+12,yy-21)],C['green'],3)
    # headphones overlay
    for side in [-1,1]:
        xx=cx+side*91
        a.box((xx-18,cy-12,xx+18,cy+57),'#12392e',ink,5,12)
        a.ellipse((xx-12,cy+3,xx+12,cy+44),C['green'],ink,3)
        a.stroke([(xx-5,cy+15),(xx+5,cy+33)],C['ink'],4)
        a.stroke([(xx+5,cy+15),(xx-5,cy+33)],C['ink'],4)
    # micro tech details
    for px,py in [(207,299),(310,299),(201,353),(306,353)]:
        a.ellipse((X(px)-2,Y(py)-2,X(px)+2,Y(py)+2),C['green'])

def cat(a,q,action,i):
    ink='#274064';cx=256+q['bodyX'];cy=213+q['bounce']+q['jump']
    phase=i/max(1,SPEC['pix'][action])*math.tau
    # tail drawn as continuous curved padded stroke (not rotated image)
    tail_end=(346+24*math.sin(phase),375-20*math.cos(phase))
    a.stroke([(cx+65,349+q['jump']),(cx+112,335+q['jump']),(tail_end[0],tail_end[1]+q['jump'])],ink,34)
    a.stroke([(cx+65,349+q['jump']),(cx+112,335+q['jump']),(tail_end[0],tail_end[1]+q['jump'])],C['cyan2'],26)
    # body, short legs
    a.ellipse((cx-73,285+q['jump'],cx+75,419+q['jump']),C['snow'],ink,5)
    a.ellipse((cx-49,318+q['jump'],cx+48,399+q['jump']),'#d8f5ff')
    stride=math.sin(phase)*24 if action in ('walk','run') else 0
    lift=8*max(0,math.cos(phase)) if action in ('walk','run') else 0
    for side in (-1,1):
        xx=cx+side*48+side*stride;by=421+q['jump']-lift*(1 if side==-1 else 0)
        a.ellipse((xx-28,by-19,xx+29,by+24),C['snow'],ink,4)
        for ix in (-10,0,10):a.stroke([(xx+ix,by+10),(xx+ix,by+16)],C['pink'],2)
    # arms/paws are separate fresh shapes each pose (drawn directly)
    left=(cx-103,334+q['jump']);right=(cx+104,334+q['jump'])
    if action in ('wave','assist_point','celebrate'):
        right=(cx+103+22*math.sin(phase),253+q['jump']+12*math.cos(phase))
    if action in ('celebrate','happy_bounce','jump'):
        left=(cx-105,259+q['jump'])
    if action in ('talk','laugh','curious'):
        right=(cx+82,300+q['jump']+10*math.sin(phase))
    for st,en in [((cx-61,313+q['jump']),left),((cx+61,313+q['jump']),right)]:
        a.stroke([st,en],ink,32)
        a.stroke([st,en],C['snow'],24)
        a.ellipse((en[0]-24,en[1]-22,en[0]+23,en[1]+23),C['snow'],ink,3)
        for dx in (-8,2,12):a.ellipse((en[0]+dx-3,en[1]-2,en[0]+dx+3,en[1]+4),C['pink'])
    # head and ears, no reuse of source bitmap
    a.ellipse((cx-114,cy-92,cx+114,cy+103),C['cyan'],ink,5)
    for sign in (-1,1):
        ex=cx+sign*84
        pts=[(ex-33,cy-59),(ex+sign*21,cy-143),(ex+38,cy-55)] if sign==1 else [(ex-38,cy-55),(ex+sign*21,cy-143),(ex+33,cy-59)]
        a.poly(pts,C['cyan'],ink,5)
        xinner=ex+sign*4
        a.poly([(xinner-18,cy-66),(xinner+sign*15,cy-119),(xinner+21,cy-60)],C['pink'])
    # eye & mouth expression
    for side in (-1,1):
        ex=cx+side*45;ey=cy+14
        if q['l_eye']=='happy':
            a.stroke([(ex-20,ey+5),(ex,ey-6),(ex+20,ey+5)],ink,5)
        elif q['l_eye']=='blink':a.stroke([(ex-22,ey),(ex+22,ey)],ink,4)
        else:
            a.ellipse((ex-26,ey-22,ex+26,ey+25),'#f6fdff',ink,4)
            a.ellipse((ex-16,ey-16,ex+17,ey+20),C['purple'],ink,2)
            a.ellipse((ex-8,ey-9,ex+10,ey+13),'#334cbd')
            a.ellipse((ex-10,ey-11,ex-2,ey-3),'white')
        a.ellipse((ex-30,ey+30,ex-10,ey+40),C['pink'])
    a.poly([(cx-7,cy+55),(cx+7,cy+55),(cx,cy+64)],'#e85a9c')
    if q['mouth']=='wide':a.ellipse((cx-15,cy+65,cx+15,cy+83),'#b9458b',ink,2)
    elif q['mouth']=='round':a.ellipse((cx-7,cy+64,cx+7,cy+78),'#bc4491',ink,2)
    else:
        a.stroke([(cx-15,cy+69),(cx-6,cy+75),(cx,cy+69),(cx+7,cy+75),(cx+16,cy+69)],ink,2)
    # headphones and neck jewel
    for side in [-1,1]:
        hx=cx+side*113
        a.ellipse((hx-19,cy-26,hx+19,cy+26),C['purple'],ink,4)
        a.ellipse((hx-12,cy-19,hx+12,cy+19),C['cyan2'],ink,2)
    a.ellipse((cx-21,cy+98,cx+21,cy+131),C['purple'],ink,4)
    a.ellipse((cx-12,cy+106,cx+12,cy+122),C['cyan2'])
    for x,y in [(-65,-30),(68,-46),(-88,31),(89,28)]:
        a.ellipse((cx+x-3,cy+y-3,cx+x+3,cy+y+3),'#e0fbff')

def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    report={'schema':'video-ai-editor/offline-original-vector-frame-prototype/v1',
            'referenceVersion':'canonical-2026-10-29',
            'technique':'per-frame-vector-redraw (no source image cutout or piecewise transformation)',
            'limits':['Simplified new vector study is not the approved detailed anime artwork',
                      'Visual identity must be approved before video production',
                      'Computer-designed pose drawings are not independently hand-painted inbetweens',
                      'Motion and lip-sync are not production reviewed'],
            'productionApproved':False,'billedExternalUsd':0,'creditsUsed':0,'characters':{}}
    for who,catalog in SPEC.items():
        report['characters'][who]={}
        for act,n in catalog.items():
            target=ROOT/who/act;target.mkdir(parents=True,exist_ok=True)
            hashes=[]
            for i in range(n):
                a=Art();q=action_pose(act,i,n,who)
                if who=='urfavxbf':host(a,q,act,i)
                else:cat(a,q,act,i)
                fn=target/f'{i:03d}.png';a.save(fn)
                hashes.append(hashlib.sha256(fn.read_bytes()).hexdigest())
            manifest={'schema':'video-ai-editor/independently-drawn-action/v1',
                      'character':who,'action':act,'sourceReference':'canonical-2026-10-29',
                      'frameCount':n,'fps':12,'loop':act not in ('jump','celebrate','point_camera','surprised'),
                      'artProvenance':'local-programmatic-whole-frame-original-vector-study',
                      'technique':'drawn-from-pose-geometry-each-frame-NOT-cutout-image-transforms',
                      'artApproved':False,'motionReviewed':False,'phonemeAligned':False,
                      'frames':[{'index':i,'filename':f'{i:03d}.png','sha256':sha} for i,sha in enumerate(hashes)]}
            (target/'manifest.json').write_text(json.dumps(manifest,indent=2))
            report['characters'][who][act]={'frames':n,'uniquePngByteCount':len(set(hashes))}
            print(who,act,n,len(set(hashes)),flush=True)
    (OUT/'STATUS.json').write_text(json.dumps(report,indent=2))
    with zipfile.ZipFile(OUT.parent / 'UrFavXBF_PIX_ZeroBudget_Vector_Frame_Studies.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=5) as z:
        for f in OUT.rglob('*'):
            if f.is_file():z.write(f,f.relative_to(OUT))
    return report
if __name__=='__main__':main()