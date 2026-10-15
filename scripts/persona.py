"""Keep the built-in original 3D reference when image tools are unavailable."""
from pathlib import Path
import shutil


def reference_artwork(output):
    source = Path(__file__).resolve().parents[1] / 'assets' / 'yearsona-style-reference.png'
    relative = 'assets/yearsona-reference.png'
    target = output.parent / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    return {'src': relative, 'alt': 'Yearsona 通用3D搪胶潮玩风格参考，非用户专属形象', 'method': 'bundled-reference', 'generation_status': 'needs-personalization'}
