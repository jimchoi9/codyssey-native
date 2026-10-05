"""외부 패키지 없이 실행하는 콘솔 프로그램 회귀 테스트."""
import contextlib
import importlib.util
import io
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load_app():
    spec = importlib.util.spec_from_file_location('prompt_manager', ROOT / 'main.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def invoke(function, *args, inputs=()):
    output = io.StringIO()
    with patch('builtins.input', side_effect=inputs), contextlib.redirect_stdout(output):
        result = function(*args)
    return result, output.getvalue()


class MenuTests(unittest.TestCase):
    def test_invalid_choices_return_to_menu_and_zero_exits(self):
        result = subprocess.run([sys.executable, '-B', str(ROOT / 'main.py')],
                                input='9\ntext\n\n-1\n0\n', text=True,
                                capture_output=True, timeout=5)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.count('=== 나만의 프롬프트 관리 ==='), 5)
        self.assertIn('잘못된 메뉴', result.stdout)
        self.assertIn('종료합니다', result.stdout)


class DataTests(unittest.TestCase):
    def test_initial_data_is_complete_and_fresh_each_run(self):
        app = load_app()
        self.assertTrue(hasattr(app, 'create_initial_prompts'))
        prompts = app.create_initial_prompts()
        self.assertGreaterEqual(len(prompts), 3)
        for prompt in prompts:
            self.assertTrue(prompt['title'].strip())
            self.assertTrue(prompt['content'].strip())
            self.assertIn(prompt['category'], app.CATEGORIES)
            self.assertIsInstance(prompt['favorite'], bool)
        prompts[0]['title'] = 'changed'
        prompts[0]['favorite'] = True
        fresh = app.create_initial_prompts()
        self.assertNotEqual(fresh[0]['title'], 'changed')
        self.assertFalse(fresh[0]['favorite'])
