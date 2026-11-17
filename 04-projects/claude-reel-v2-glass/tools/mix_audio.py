import json, subprocess, pathlib

A = pathlib.Path('/home/hatch/workspace/claude-reel-v2-assets')
B = pathlib.Path('/home/hatch/workspace/sfx-library/drive-bundle')
data = json.load(open(A / 'reel_data.json'))
scenes = data['SCENES']
vo = '/home/hatch/workspace/claude-reel/vo/vo_final.wav'

inputs = ['-i', vo, '-i', str(A / 'wallpaper.mp3'),
          '-i', str(B / 'Fast Whoosh Sound Effect.mp3'),
          '-i', str(B / 'Pop 1.mp3'),
          '-i', str(B / 'Mario Coin Sound - Sound Effect (HD).mp3')]
fc = []
# music bed: offset 10s into the track, -21 dB, fades
fc.append('[1:a]atrim=10:69.2,asetpts=PTS-STARTPTS,volume=0.089,afade=t=in:st=0:d=0.5,afade=t=out:st=56.7:d=2.5[mus]')
labels = ['[0:a]', '[mus]']
# whoosh on every scene transition (scenes 2..15 starts)
for i, s in enumerate(scenes[1:], start=1):
    t = max(0.0, s['t0'] - 0.05)
    lab = f'w{i}'
    fc.append(f'[2:a]atrim=0:1.1,asetpts=PTS-STARTPTS,volume=0.30,adelay={int(t*1000)}|{int(t*1000)}[{lab}]')
    labels.append(f'[{lab}]')
# pops: L2 price stamp, L15 CTA
for j, t in enumerate([4.05, 51.25]):
    lab = f'p{j}'
    fc.append(f'[3:a]atrim=0:0.5,asetpts=PTS-STARTPTS,volume=0.5,adelay={int(t*1000)}|{int(t*1000)}[{lab}]')
    labels.append(f'[{lab}]')
# coin sfx at the payoff
for j, t in enumerate([35.38, 36.55]):
    lab = f'c{j}'
    fc.append(f'[4:a]atrim=0:0.9,asetpts=PTS-STARTPTS,volume=0.42,adelay={int(t*1000)}|{int(t*1000)}[{lab}]')
    labels.append(f'[{lab}]')
fc.append(''.join(labels) + f'amix=inputs={len(labels)}:normalize=0[mixed]')
fc.append('[mixed]loudnorm=I=-14:TP=-2.0:LRA=11,aresample=48000[out]')
cmd = ['ffmpeg', '-y'] + inputs + ['-filter_complex', ';'.join(fc), '-map', '[out]', '-t', '59.2', str(pathlib.Path('/home/hatch/workspace/claude-reel-v2/film/assets/final_mix.wav'))]
print(' '.join(cmd[:3]), '... inputs:', len(inputs)//2)
r = subprocess.run(cmd, capture_output=True, text=True)
print(r.returncode, r.stderr[-500:] if r.returncode else 'MIX OK')
