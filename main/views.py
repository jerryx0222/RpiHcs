import subprocess
from pathlib import Path

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST


@login_required
def home(request):
    return render(request, 'main/home.html')


@login_required
@require_POST
def start_unraid(request):
    # The script path comes only from settings, never from the request.
    script = Path(settings.UNRAID_SCRIPT)
    if not script.is_file():
        return JsonResponse({'ok': False, 'output': f'找不到腳本：{script}'}, status=500)
    try:
        r = subprocess.run(
            ['/bin/bash', str(script)],
            capture_output=True, text=True,
            timeout=settings.UNRAID_SCRIPT_TIMEOUT,
            cwd=script.parent,
        )
    except subprocess.TimeoutExpired:
        return JsonResponse({'ok': False, 'output': f'執行逾時（{settings.UNRAID_SCRIPT_TIMEOUT} 秒）'}, status=504)
    output = (r.stdout + r.stderr)[-2000:]
    return JsonResponse({'ok': r.returncode == 0, 'returncode': r.returncode, 'output': output})
