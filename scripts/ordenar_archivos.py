"""Orden seguro App Inventario. Sin argumentos informa; --aplicar mueve candidatos; --revertir restaura MANIFIESTO."""
import shutil, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
DEST=ROOT/'historico'/'2026-11-04-orden'
BACKUP=Path(r'E:\_ARCHIVO_FERRETERIA\app-inventario-antes_2026-11-04c')
PROTECTED={'index.html','app.js','style.css','planos_generated.js','generar_planos.js','AGENTS.md','CLAUDE.md','README.md','ACTUALIZAR_GITHUB_APP_INVENTARIO.bat','MEMORIA_PROYECTO.md'}
def rel(p): return str(p.relative_to(ROOT)).replace('/','\\')
def text_files():
    for p in ROOT.rglob('*'):
        if p.is_file() and not any(x in {'.git','historico','node_modules'} for x in p.relative_to(ROOT).parts):
            if p.suffix.lower() in {'.md','.txt','.html','.js','.py','.bat','.json'}: yield p
def candidates():
    out=[]
    for pat in ('__pycache__','logs','log','*backup*','*respaldo*','*copia*','*.bak'):
        out.extend(ROOT.glob(pat))
    return sorted({p for p in out if p.exists() and p.name not in PROTECTED and p.name not in {'scripts','docs'}},key=str)
def refs(name):
    ans=[]
    for p in text_files():
        try:
            if name.lower() in p.read_text(encoding='utf-8',errors='ignore').lower(): ans.append(rel(p))
        except OSError: pass
    return ans
def actions(): return [(p,refs(p.name)) for p in candidates()]
def apply(rows):
    DEST.mkdir(parents=True,exist_ok=True); lines=['# Manifiesto App Inventario','', 'Fecha: 2026-11-04','Revertir: python scripts\\ordenar_archivos.py --revertir MANIFIESTO.md','', '| origen | destino | respaldo |','|---|---|---|']
    moved=0
    for p,r in rows:
        if r: continue
        target=DEST/p.name
        if target.exists(): continue
        shutil.move(str(p),str(target)); lines.append(f'| `{rel(p)}` | `{rel(target)}` | `{BACKUP/p.name}` |'); moved+=1
    (DEST/'MANIFIESTO.md').write_text('\n'.join(lines)+'\n',encoding='utf-8'); print(f'Movidos: {moved}; manifiesto: {DEST/"MANIFIESTO.md"}')
def revert(man):
    moved=0
    for line in Path(man).read_text(encoding='utf-8').splitlines():
        if not line.startswith('| `'): continue
        a,b=[x.strip().strip('`') for x in line.strip('|').split('|')[:2]]; src=ROOT/b; dst=ROOT/a
        if src.exists() and not dst.exists(): dst.parent.mkdir(parents=True,exist_ok=True); shutil.move(str(src),str(dst)); moved+=1
    print(f'Revertidos: {moved}')
if __name__=='__main__':
    if '--revertir' in sys.argv: revert(sys.argv[sys.argv.index('--revertir')+1]); sys.exit()
    rows=actions(); print('== INFORME (no mueve nada)')
    for p,r in rows: print(f'{rel(p)} | referencias={";".join(r) if r else "NINGUNA"}')
    if '--aplicar' in sys.argv: apply(rows)
