"""Cross-platform regression coverage for the formerly missing persona delivery."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
from render_report import demo_data


class DeliveryTests(unittest.TestCase):
    def run_renderer(self, *args):
        return subprocess.run([sys.executable, '-X', 'utf8', str(SCRIPTS / 'render_report.py'), *map(str, args)], capture_output=True, text=True, encoding='utf-8')

    def test_report_automatically_delivers_character_and_card(self):
        with tempfile.TemporaryDirectory(prefix='yearsona 中文 space ') as tmp:
            folder = Path(tmp)
            output = folder / 'report.html'
            result = self.run_renderer('--demo', '--output', output)
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads((folder / 'report.prepared.json').read_text(encoding='utf-8'))
            character = folder / data['artwork']['src']
            self.assertEqual(character.read_bytes()[:8], b'\x89PNG\r\n\x1a\n')
            self.assertEqual(data['artwork']['method'], 'bundled-reference')
            self.assertEqual(data['artwork']['generation_status'], 'needs-personalization')
            self.assertTrue((folder / data['share_card']['html']).is_file())
            html = output.read_text(encoding='utf-8')
            self.assertIn('persona-loader', html)
            self.assertNotIn('__ANNUAL_REVIEW_', html)
            self.assertEqual(self.run_renderer('--demo', '--output', output).returncode, 2)

    def test_existing_generated_image_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / 'generated.png').write_bytes((SCRIPTS.parent / 'assets/yearsona-style-reference.png').read_bytes())
            data = demo_data()
            data['artwork'] = {'src': 'generated.png', 'alt': '原创角色', 'method': 'image-tool', 'generation_status': 'complete'}
            source = folder / 'input.json'
            source.write_text(json.dumps(data), encoding='utf-8')
            result = self.run_renderer('--data', source, '--output', folder / 'report.html')
            self.assertEqual(result.returncode, 0, result.stderr)
            prepared = json.loads((folder / 'report.prepared.json').read_text(encoding='utf-8'))
            self.assertEqual(prepared['artwork'], data['artwork'])

    def test_missing_image_is_an_actionable_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            data = demo_data()
            data['artwork'] = {'src': 'missing.png'}
            source = folder / 'input.json'
            source.write_text(json.dumps(data), encoding='utf-8')
            result = self.run_renderer('--data', source, '--output', folder / 'report.html')
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('artwork asset is missing', result.stderr)

    def test_reference_is_explicitly_unfinished(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'preview.html'
            result = self.run_renderer('--demo', '--output', output)
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads(output.with_suffix('.prepared.json').read_text(encoding='utf-8'))
            self.assertNotEqual(data['artwork']['generation_status'], 'complete')
            self.assertIn('通用3D风格参考 · 专属形象待生成', output.read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
