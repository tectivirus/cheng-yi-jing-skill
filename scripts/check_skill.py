#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""仓库自检：结构、frontmatter、六段、禁词、manifest、附录索引。"""
import io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = 'celebrity-cheng-yi-jing'
FILES = ['SKILL.md', 'work.md', 'persona.md', 'work_skill.md', 'persona_skill.md', 'meta.json', 'manifest.json']
SIX = ['subject_definitions', 'summary', 'retention_analysis', 'detailed_description',
       'overall_soundscape', 'non_diegetic_music']
FORBIDDEN = ['米哥']
fails = []

def rd(n):
    with io.open(os.path.join(ROOT, n), 'rb') as f:
        raw = f.read()
    if raw.startswith(b'\xef\xbb\xbf'):
        fails.append(n + ': BOM')
    # 统一换行：Windows 上脚本写出的文件是 CRLF，正则里的 $ 会因此失配
    return raw.decode('utf-8').replace('\r\n', '\n').replace('\r', '\n')

for f in FILES:
    if not os.path.isfile(os.path.join(ROOT, f)):
        fails.append('missing ' + f)
if fails:
    print('FAIL', fails); sys.exit(1)

skill = rd('SKILL.md')
m = re.match(r'\A---\r?\n(.*?)\r?\n---\r?\n', skill, re.S)
if not m:
    fails.append('SKILL.md: frontmatter 缺失')
else:
    fm = m.group(1)
    for k in ('name:', 'description:', 'user-invocable:'):
        if k not in fm:
            fails.append('frontmatter 缺 ' + k)
    got = re.search(r'^name:\s*(.+)$', fm, re.M)
    if got and got.group(1).strip() != NAME:
        fails.append('name 应为 ' + NAME)

for token in ('PART A', 'PART B', 'Layer 0', '运行规则', '程一镜'):
    if token not in skill:
        fails.append('SKILL.md 缺 ' + token)
for s in SIX:
    if s not in skill:
        fails.append('六段缺 ' + s)
for w in FORBIDDEN:
    for f in FILES:
        if w in rd(f):
            fails.append(f + ' 含禁词 ' + w)

idx = skill.count('语料章节索引')
rows = len(re.findall(r'(?m)^- .+ · L\d+$', skill))
if idx == 0:
    fails.append('缺语料章节索引')
if rows < 100:
    fails.append('索引条数异常: %d' % rows)

mf = json.loads(rd('manifest.json'))
for need in ('SKILL.md', 'work_skill.md', 'persona_skill.md'):
    if need not in mf.get('artifacts', []):
        fails.append('manifest.artifacts 缺 ' + need)
meta = json.loads(rd('meta.json'))
if meta.get('slug') != 'cheng-yi-jing':
    fails.append('meta.slug 应为 cheng-yi-jing')

print('files:', ', '.join(FILES))
print('six sections:', len(SIX), 'ok' if not any('六段缺' in f for f in fails) else 'fail')
print('index rows:', rows)
print('checks:', 'PASS' if not fails else 'FAIL')
for f in fails:
    print(' -', f)
sys.exit(1 if fails else 0)