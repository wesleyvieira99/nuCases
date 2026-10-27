"""Build the dependency-free, offline Staff Lab document from local source data."""
from pathlib import Path
import json
import re
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'downloads'
DATA_DIR = ROOT / 'data'
DATA_DIR.mkdir(exist_ok=True)
OUT.mkdir(exist_ok=True)
data = {}
for name in ('research', 'curriculum', 'simulations', 'syntax', 'java'):
    data[name] = json.loads((DATA_DIR / f'{name}.json').read_text())

cases = data['simulations']
if isinstance(cases, dict):
    cases = cases.get('simulations', cases.get('cases'))
    data['simulations'] = cases
assert len(cases) == 60
assert len({c['id'] for c in cases}) == 60
assert len({c['title'] for c in cases}) == 60
for c in cases:
    assert len(c['rounds']) == 4, c['id']
    assert sum(r['minutes'] for r in c['rounds']) == 120, c['id']
    assert all(r['prompt'] and r['strongAnswer'] and r['followups'] for r in c['rounds'])
    assert len(c['solution']['tests']) >= 4
    assert len(c['rubric']) >= 4
curriculum = data['curriculum']
assert len(curriculum['modules']) >= 20
assert len(curriculum['codeLabs']) >= 14
assert len(curriculum['flashcards']) >= 80
assert len(curriculum['plan']) >= 12
for kind in ('modules', 'codeLabs', 'flashcards'):
    assert len({x['id'] for x in curriculum[kind]}) == len(curriculum[kind]), kind
syntax = data['syntax']
assert len(syntax['drills']) >= 36
assert len(syntax['recipes']) >= 12
for drill in syntax['drills']:
    placeholders = set(re.findall(r'\{\{([^}]+)\}\}', drill['skeleton']))
    keys = {s['key'] for s in drill['slots']}
    assert placeholders == keys, drill['id']
    assert all(s['answers'] for s in drill['slots']), drill['id']
java = data['java']
assert len(java['cards']) >= 56
assert len({c['id'] for c in java['cards']}) == len(java['cards'])
for card in java['cards']:
    assert all(card.get(k) for k in ('id', 'title', 'category', 'question', 'answer', 'code', 'memory', 'pitfall', 'sourceUrl', 'validation'))
    assert 'public class Main' in card['code']
sources = {s['id'] for s in data['research']['sources']}
for f in data['research']['findings'] + data['research']['process']:
    assert set(f.get('sourceIds', [])) <= sources

payload = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\/')
html = (ROOT / 'src' / 'shell.html').read_text().replace('/*__CSS__*/', (ROOT / 'src' / 'style.css').read_text()).replace('/*__JS__*/', (ROOT / 'src' / 'java.js').read_text()+'\n'+(ROOT / 'src' / 'app.js').read_text()).replace('__DATA__', payload)
assert not re.search(r'__(?:CSS|JS|DATA)__', html)
(ROOT / 'index.html').write_text(html)

extensions = {'python': 'py', 'kotlin': 'kt', 'java': 'java', 'clojure': 'clj', 'typescript': 'ts', 'sql': 'sql'}
with zipfile.ZipFile(OUT / 'codigos-e-receitas.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
    archive.writestr('LEIA-PRIMEIRO.txt', 'STAFF LAB — CÓDIGOS DE ESTUDO\n\nLeia o contexto e o comando de execução em cada pasta. Alguns exemplos requerem um banco ou dependências locais. O arquivo de testes pode conter instruções em linguagem natural; veja o contrato do lab. Não são exemplos de produção nem perguntas oficiais do Nubank.\n\nAbra index.html para a experiência completa. Pesquisa: 26/10/2026.\n')
    for n, lab in enumerate(curriculum['codeLabs'], 1):
        slug = re.sub(r'[^a-zA-Z0-9_-]+', '-', str(lab['id']))
        folder = f'laboratorios/{n:02d}-{slug}'
        ext = extensions.get(lab['language'].lower(), 'txt')
        match = re.search(r'em ([A-Za-z0-9_]+\.(?:py|kt|java|clj|ts|sql))', str(lab['run']))
        filename = match.group(1) if match else f'referencia.{ext}'
        archive.writestr(f'{folder}/{filename}', lab['code']+'\n\n'+str(lab['tests']))
        archive.writestr(f'{folder}/COMO-RODAR.txt', lab['title']+'\n\n'+str(lab['run'])+'\n\nValidação: '+str(lab.get('validation', 'Ver portal')))
        archive.writestr(f'{folder}/contexto.json', json.dumps({k: v for k, v in lab.items() if k != 'code'}, ensure_ascii=False, indent=2))
    for n, recipe in enumerate(syntax['recipes'], 1):
        archive.writestr(f'receitas/{n:02d}-{recipe["id"]}.txt', recipe['title']+'\n\n'+str(recipe['context'])+'\n\n'+recipe['code']+'\n\nReferência: '+recipe['sourceUrl'])
    for card in java['cards']:
        folder = 'java-de-cabeca/' + card['id']
        archive.writestr(folder + '/Main.java', card['code'])
        archive.writestr(folder + '/COMO-RODAR.txt', card['title'] + '\n\n' + card['question'] + '\n\njavac --release 17 Main.java\njava -ea Main\n\n' + card['validation'] + '\n\n' + card['sourceUrl'])
print(json.dumps({'html_bytes': len(html.encode()), 'modules': len(curriculum['modules']), 'lessons': sum(len(x['lessons']) for x in curriculum['modules']), 'simulations': len(cases), 'rounds': sum(len(x['rounds']) for x in cases), 'labs': len(curriculum['codeLabs']), 'drills': len(syntax['drills']), 'recipes': len(syntax['recipes']), 'flashcards': len(java['cards']) + len(curriculum['flashcards']) + sum(len(x.get('flashcards', [])) for x in cases), 'java_cards': len(java['cards']), 'sources': len(sources)}, ensure_ascii=False))
