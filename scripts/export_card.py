"""Export the local 9:16 card with optional Playwright on macOS, Windows or Linux."""
import argparse
import base64
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--html', type=Path, required=True)
    parser.add_argument('--png', type=Path, required=True)
    parser.add_argument('--data', type=Path, help='Prepared JSON to read; writes a separate .exported.json')
    parser.add_argument('--browser-executable', type=Path)
    parser.add_argument('--force', action='store_true')
    args = parser.parse_args()
    if not args.html.is_file():
        parser.error('card HTML does not exist')
    if args.png.suffix.lower() != '.png' or args.png.resolve() == args.html.resolve():
        parser.error('output must be a separate PNG file')
    exported = args.data.with_name(args.data.stem + '.exported.json') if args.data else None
    if not args.force and (args.png.exists() or (exported and exported.exists())):
        parser.error('output exists; choose a new filename or use --force')
    data = json.loads(args.data.read_text(encoding='utf-8-sig')) if args.data else None
    if data is not None:
        try:
            relative = args.png.resolve().relative_to(args.data.parent.resolve()).as_posix()
        except ValueError:
            parser.error('PNG must be inside the prepared-data directory')
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        parser.error('Install optional export support with: python3 -m pip install playwright; python3 -m playwright install chromium (Windows: use python)')
    args.png.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as play:
        options = {'headless': True}
        if args.browser_executable:
            options['executable_path'] = str(args.browser_executable.expanduser().resolve())
        browser = play.chromium.launch(**options)
        try:
            page = browser.new_page(viewport={'width': 1080, 'height': 1920}, device_scale_factor=1, reduced_motion='reduce')
            page.goto(args.html.resolve().as_uri(), wait_until='load')
            page.evaluate('document.fonts.ready')
            page.evaluate('Promise.all([...document.images].map(i => i.decode()))')
            page.locator('.card').screenshot(path=str(args.png))
        finally:
            browser.close()
    if data is not None:
        data.setdefault('share_card', {}).update({'image': relative, 'download_data': 'data:image/png;base64,' + base64.b64encode(args.png.read_bytes()).decode('ascii')})
        exported.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
        print(str(exported.resolve()))
    print(str(args.png.resolve()))


if __name__ == '__main__':
    main()
