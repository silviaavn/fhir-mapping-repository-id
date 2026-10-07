# Bungkus keluaran build_h.py (crosscheck.html) menjadi docs/index.html untuk GitHub Pages
#   python src/make_pages.py [crosscheck.html] [docs/index.html]
import sys, os, pathlib
_ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRCP=sys.argv[1] if len(sys.argv)>1 else os.path.join(_ROOT,"crosscheck.html")
DSTP=sys.argv[2] if len(sys.argv)>2 else os.path.join(_ROOT,"docs","index.html")
SRC=pathlib.Path(SRCP).read_text()
HEAD=('<!doctype html>\n<html lang="id">\n<head>\n<meta charset="utf-8">\n'
 '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
 '<meta name="description" content="Konsolidasi playbook interoperabilitas SATUSEHAT: variabel, elemen FHIR, '
 'crosscheck antar use case, ringkasan resource, dan Lampiran Standar Terminologi.">\n')
i=SRC.index('</style>')+len('</style>')
out=HEAD+SRC[:i]+'\n</head>\n<body>'+SRC[i:]+'\n</body>\n</html>\n'
assert out.count('<body>')==1
pathlib.Path(DSTP).write_text(out)
print(DSTP, len(out))
