"""Regenerate English scientific figures from recorded numerical evidence."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT
OUT=ROOT/'paper/figures'
OUT.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False})
BLUE='#237fa2';RED='#c75546';BLACK='#293641'
def save(fig,name):
    for suffix in ('png','svg'):
        fig.savefig(OUT/f'{name}.{suffix}',dpi=300,bbox_inches='tight')
    plt.close(fig)

fig,axs=plt.subplots(1,4,figsize=(11.6,3.1))
for ax in axs:
    ax.set(aspect='equal',xlim=(-14,14),ylim=(-15,15));ax.axis('off')
ax=axs[0]
pts=[(0,0,'N')]
for n,r in ((6,5),(12,10)):
    for i in range(n):
        a=np.pi-2*np.pi*i/n
        first='S' if n==6 else 'N'
        pole=first if i%2==0 else ('N' if first=='S' else 'S')
        pts.append((r*np.cos(a),r*np.sin(a),pole))
for x,y,p in pts:
    ax.add_patch(Circle((x,y),2,fc=RED if p=='N' else BLUE,ec='white',lw=.7))
    ax.text(x,y,p,ha='center',va='center',color='white',fontsize=6)
ax.set_title('(a) Concentric array\nCCA, 19 discs')
ax.text(0,-14,'Disc diameter 4 mm',ha='center',fontsize=8)
ax=axs[1]
for i,x in enumerate(np.arange(-10,11,5)):
    for j,y in enumerate(np.arange(-10,11,5)):
        p=(i+j)%2;ax.add_patch(Circle((x,y),2.5,fc=RED if not p else BLUE,ec='white',lw=.7))
        ax.text(x,y,'N' if not p else 'S',ha='center',va='center',color='white',fontsize=6)
ax.set_title('(b) Checkerboard array\nCPA, 25 discs');ax.text(0,-14,'Disc diameter 5 mm',ha='center',fontsize=8)
ax=axs[2]
for i in range(10):ax.add_patch(Rectangle((-10,-12+i*2.4),20,2.4,fc=RED if i%2==0 else BLUE,ec='white',lw=.5))
ax.set_title('(c) Parallel stripes\nPSM-L and PSM-H');ax.text(0,-14,'Isolation 2.5 / 4.5 mm',ha='center',fontsize=8)
ax=axs[3];ax.axis('on');ax.set(xlim=(-12,12),ylim=(-12,12),xlabel='X (mm)',ylabel='Y (mm)')
ax.add_patch(Rectangle((-10,-10),20,20,fc='#eff4f6',ec='#8b959c',ls='--'))
for j,(x,y) in enumerate([(-7.594,7.594),(-7.594,-7.594),(7.594,7.594),(7.594,-7.594),(0,1.406)],1):
    ax.plot(x,y,'s',color=BLACK,ms=6);ax.text(x+.5,y+.7,str(j),fontsize=7)
ax.plot(0,0,'+',color='black');ax.set_title('(d) Five triaxial nodes\n15 magnetic channels')
fig.tight_layout(w_pad=1.1);save(fig,'Fig1_geometry')

fig=plt.figure(figsize=(10.7,4.2));ax=fig.add_axes([.055,.15,.32,.76])
x,y=np.meshgrid(np.arange(-10,11),np.arange(-10,11));ax.scatter(x,y,s=5,c='#acb6bc')
x,y=np.meshgrid(np.arange(-10,11,2),np.arange(-10,11,2));ax.scatter(x,y,s=22,fc='none',ec=BLUE,lw=.7)
ax.set(aspect='equal',xlabel='X (mm)',ylabel='Y (mm)',title='Same-source 1 and 2 mm grids');ax.grid(alpha=.13)
fig.text(.43,.91,'One indentation → one steady 15-channel sample',fontsize=11,weight='bold')
for i,s in enumerate(['Unloaded baseline → indent → hold → release',
                       'Dense map: 441 locations; sparse subset: 121',
                       'Reserved repeat: 441 new contacts, no fitting',
                       'Independent motion: recorded magnetic time series']):
    fig.text(.44,.79-i*.15,s,fontsize=10)
fig.text(.43,.12,'Static error and dynamic error are evaluated separately.',fontsize=9,color=BLUE)
save(fig,'Fig2_protocol')

fields=json.loads((SOURCE/'models/same_source_field_diagnostics.json').read_text(encoding='utf8'))
keys=['19C','5x5','flot1650-2.5mm','flot1650-4.5mm'];labels=['CCA','CPA','PSM-L','PSM-H']
fig,axs=plt.subplots(1,3,figsize=(10.8,3.3))
for ax,metric,label,title in [
    (axs[0],'xy_mae_mm','Planar mean error (mm)','(a) Unseen positions'),
    (axs[1],'p10_whitened_sigma_min_per_mm','Weak-direction P10 (1/mm)','(b) Spatial distinguishability')]:
    vals=[fields[k]['frozen_validation' if metric=='xy_mae_mm' else 'field_observability'][metric] for k in keys]
    bars=ax.bar(labels,vals,color=['#91abb5',BLUE,'#91abb5','#91abb5'],width=.65)
    ax.bar_label(bars,fmt='%.2f',padding=3,fontsize=8);ax.set(ylabel=label,title=title,ylim=(0,max(vals)*1.22));ax.grid(axis='y',alpha=.14)
ax=axs[2];bars=ax.bar(['SC-RBF\n2 mm','DC-RBF\n1 mm'],[.349466985,.288394377],color=['#91abb5',BLUE],width=.5)
ax.bar_label(bars,fmt='%.3f',padding=3);ax.set(ylabel='Planar mean error (mm)',title='(c) Same reserved 441 contacts',ylim=(0,.45));ax.grid(axis='y',alpha=.14)
fig.tight_layout(w_pad=1.8);save(fig,'Fig3_static_results')

rows={r['trial_id']:r for r in json.loads((SOURCE/'data/dynamic/analysis_results.json').read_text(encoding='utf8'))}
fig=plt.figure(figsize=(10.3,6.6));row=rows[32];m=row['motion'];colors=[BLUE,RED]
ax=fig.add_subplot(2,2,1,projection='3d')
for j,s in enumerate(m['segments']):
    p=np.array(s['prediction']);q=np.array(s['reference'])
    if j==0:ax.plot(*q.T,'k--',lw=1,label='Command reference')
    ax.plot(*p.T,color=colors[j],lw=.9,label=f'Repeat {j+1}')
ax.view_init(23,20);ax.set(xlabel='X (mm)',ylabel='Y (mm)',zlabel='Z (mm)',title='(a) Simultaneous XYZ contact');ax.legend(fontsize=7)
for axis in range(3):
    ax=fig.add_subplot(2,2,axis+2)
    for j,s in enumerate(m['segments']):
        p=np.array(s['prediction']);q=np.array(s['reference']);t=np.array(s['t_ns'],float);t=(t-t[0])/1e9
        ax.plot(t,p[:,axis],color=colors[j],lw=.9,label=f'Repeat {j+1}')
        if j==0:ax.plot(t,q[:,axis],'k--',lw=1,label='Command reference')
    ax.set(xlabel='Time from motion start (s)',ylabel=f'{"XYZ"[axis]} (mm)',title=f'({chr(98+axis)}) {"XYZ"[axis]} response');ax.grid(alpha=.15);ax.legend(fontsize=7)
fig.tight_layout(h_pad=2,w_pad=2);save(fig,'Fig4_xyz')

fig,axs=plt.subplots(1,2,figsize=(9.3,4.1))
for ax,k,mkey in [(axs[0],17,'motion'),(axs[1],18,'arc_with_command_holds')]:
    seen=set()
    for s in rows[k][mkey]['segments']:
        if not s['n']:continue
        q=np.array(s['reference']);p=np.array(s['prediction']);j=int(s['repeat'])-1
        ax.plot(*q[:,:2].T,color='black',ls='--',lw=.6,label='Command reference' if not seen else None)
        ax.plot(*p[:,:2].T,color=colors[j],lw=.8,label=f'Repeat {j+1}' if j not in seen else None);seen.add(j)
    ax.set(xlabel='X (mm)',ylabel='Y (mm)',aspect='equal');ax.grid(alpha=.15);ax.legend(fontsize=7)
axs[0].set_title('(a) Eight directions, radius 4 mm\nPlanar error 0.453 mm; coverage 100%')
axs[1].set_title('(b) Segmented circle, radius 2 mm\nFull-contact error 0.390 mm; coverage 100%')
fig.tight_layout(w_pad=3);save(fig,'Fig5_radial_circle')

# Graphical abstract is a scientific summary, not a generated experimental image.
fig=plt.figure(figsize=(10.5,3.2));ax=fig.add_axes([.01,.04,.31,.88]);ax.imshow(plt.imread(OUT/'Fig1_geometry.png'));ax.axis('off')
fig.text(.35,.79,'15 magnetic channels',fontsize=15,weight='bold')
fig.text(.35,.60,'Baseline → normalized map → XYZ',fontsize=12)
fig.text(.35,.37,'Static planar error   0.288 mm',fontsize=13,color=BLUE)
fig.text(.35,.20,'XYZ path mean error   0.569 mm',fontsize=13,color=BLUE)
fig.text(.35,.055,'Different evaluation tasks; command-referenced motion',fontsize=9)
save(fig,'Graphical_abstract')
print('Created six English figure sets.')
