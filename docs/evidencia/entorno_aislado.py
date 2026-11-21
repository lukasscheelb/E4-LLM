"""Prueba de aislamiento OS y ejecución real de pytest dentro de Docker."""
import json
import os
import platform
import socket
import subprocess
import sys
from pathlib import Path

label = sys.argv[1]
target = sys.argv[2] if len(sys.argv) > 2 else 'tests'
interfaces = sorted(p.name for p in Path('/sys/class/net').iterdir())
routes = Path('/proc/net/route').read_text()
assert interfaces == ['lo'], interfaces
assert not any(line.split()[0] != 'lo' for line in routes.splitlines()[1:] if line.strip()), routes
try:
    with socket.create_connection(('1.1.1.1', 53), timeout=2):
        raise AssertionError('Conexion externa disponible: aislamiento no acreditado')
except OSError as error:
    blocked = {'tipo': type(error).__name__, 'mensaje': str(error), 'errno': error.errno}
metadata = {'python': sys.version, 'platform': platform.platform(), 'interfaces': interfaces,
            'rutas': routes, 'conexion_externa_bloqueada': blocked,
            'pytest': subprocess.check_output([sys.executable, '-m', 'pytest', '--version'], text=True).strip(),
            'enfoque': os.environ.get('MIRA_ENFOQUE'), 'objetivo': target}
Path('/evidence/' + label + '-entorno.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2))
print(json.dumps(metadata, ensure_ascii=False), flush=True)
command = [sys.executable, '/audit/.github/skills/pytest-runner/scripts/run_pytest.py', target,
           '--junitxml', '/evidence/' + label + '-junit.xml']
result = subprocess.run(command, check=False)
Path('/evidence/' + label + '-exit.txt').write_text(str(result.returncode) + '\n')
raise SystemExit(result.returncode)
