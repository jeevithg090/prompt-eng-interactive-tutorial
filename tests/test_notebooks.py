"""Smoke checks for the tutorial notebooks and hint modules.

None of these tests need an API key or AWS credentials. The execution test swaps the
real ``anthropic`` package for a small offline stub (see ``tests/stubs``).
"""

import importlib.util
import os
import re
import sys
from pathlib import Path

import nbformat
import pytest
from IPython.core.inputtransformer2 import TransformerManager

ROOT = Path(__file__).resolve().parents[1]
FIRST_PARTY = ROOT / "Anthropic 1P"
BEDROCK = ROOT / "AmazonBedrock"
STUBS = Path(__file__).resolve().parent / "stubs"

ALL_NOTEBOOKS = sorted(ROOT.glob("**/*.ipynb"))
FIRST_PARTY_NOTEBOOKS = sorted(FIRST_PARTY.glob("*.ipynb"))


def _ids(paths):
    return [str(p.relative_to(ROOT)) for p in paths]


def _code_cells(nb):
    return [(i, c) for i, c in enumerate(nb.cells) if c.cell_type == "code"]


def _load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_notebooks_found():
    assert len(FIRST_PARTY_NOTEBOOKS) == 13
    assert len(list((BEDROCK / "anthropic").glob("*.ipynb"))) == 14
    assert len(list((BEDROCK / "boto3").glob("*.ipynb"))) == 14


@pytest.mark.parametrize("path", ALL_NOTEBOOKS, ids=_ids(ALL_NOTEBOOKS))
def test_notebook_is_valid_nbformat(path):
    nb = nbformat.read(path, as_version=4)
    nbformat.validate(nb)


@pytest.mark.parametrize("path", ALL_NOTEBOOKS, ids=_ids(ALL_NOTEBOOKS))
def test_code_cells_compile(path):
    """Every code cell must be valid Python once IPython magics are translated."""
    nb = nbformat.read(path, as_version=4)
    transformer = TransformerManager()
    for index, cell in _code_cells(nb):
        source = transformer.transform_cell(cell.source)
        try:
            compile(source, f"{path.name}[cell {index}]", "exec")
        except SyntaxError as exc:  # pragma: no cover - failure path
            pytest.fail(f"{path.name} cell {index} does not compile: {exc}")


@pytest.mark.parametrize("path", ALL_NOTEBOOKS, ids=_ids(ALL_NOTEBOOKS))
def test_no_committed_outputs(path):
    """Notebooks are committed clean so learners see their own results."""
    nb = nbformat.read(path, as_version=4)
    for index, cell in _code_cells(nb):
        assert not cell.get("outputs"), f"{path.name} cell {index} has saved outputs"
        assert cell.get("execution_count") is None, f"{path.name} cell {index} has an execution count"


SECRET_PATTERNS = [
    re.compile(r"sk-ant-[A-Za-z0-9_-]{10,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
]


@pytest.mark.parametrize("path", ALL_NOTEBOOKS, ids=_ids(ALL_NOTEBOOKS))
def test_no_hardcoded_credentials(path):
    text = path.read_text(encoding="utf-8")
    for pattern in SECRET_PATTERNS:
        assert not pattern.search(text), f"{path.name} looks like it contains a credential"


@pytest.mark.parametrize("path", FIRST_PARTY_NOTEBOOKS, ids=_ids(FIRST_PARTY_NOTEBOOKS))
def test_first_party_notebooks_use_no_retired_claude_3_models(path):
    """Claude 3 model IDs are retired on the Claude API and return errors."""
    for _, cell in _code_cells(nbformat.read(path, as_version=4)):
        code = "\n".join(line.split("#", 1)[0] for line in cell.source.splitlines())
        assert not re.search(r"claude-3[-.]", code), f"{path.name} still calls a Claude 3 model"


@pytest.mark.parametrize("path", FIRST_PARTY_NOTEBOOKS, ids=_ids(FIRST_PARTY_NOTEBOOKS))
def test_first_party_sdk_install_is_pinned_below_1(path):
    """The lessons pass ``temperature``; anthropic 1.x+ removes it from ``messages.create``."""
    for _, cell in _code_cells(nbformat.read(path, as_version=4)):
        for line in cell.source.splitlines():
            if "pip install" in line and "anthropic" in line:
                assert '"anthropic>=0.40,<1"' in line, f"{path.name}: unpinned SDK install: {line}"


def _hint_names(paths, pattern):
    names = set()
    for path in paths:
        for _, cell in _code_cells(nbformat.read(path, as_version=4)):
            names.update(pattern.findall(cell.source))
    return names


def test_first_party_hints_exist():
    hints = _load_module(FIRST_PARTY / "hints.py", "first_party_hints")
    names = _hint_names(FIRST_PARTY_NOTEBOOKS, re.compile(r"from hints import (\w+)"))
    assert names, "expected the notebooks to import hints"
    missing = sorted(n for n in names if not isinstance(getattr(hints, n, None), str))
    assert not missing, f"hints referenced by notebooks but missing from hints.py: {missing}"


def test_bedrock_hints_exist():
    hints = _load_module(BEDROCK / "utils" / "hints.py", "bedrock_hints")
    notebooks = sorted(BEDROCK.glob("**/*.ipynb"))
    names = _hint_names(notebooks, re.compile(r"\bhints\.(\w+)"))
    assert names, "expected the notebooks to reference hints"
    missing = sorted(n for n in names if not isinstance(getattr(hints, n, None), str))
    assert not missing, f"hints referenced by notebooks but missing from utils/hints.py: {missing}"


# Errors that the lessons trigger on purpose, or that only happen because the offline
# stub returns plain text instead of a real model answer.
EXPECTED_ERRORS = {
    # Chapter 1 deliberately sends malformed Messages API requests.
    "01_Basic_Prompt_Structure.ipynb": {8: "TypeError", 10: "TypeError", 29: "TypeError", 30: "TypeError"},
    # The tool-use parser looks for a function call that the stub never produces,
    # so the cells that use its result fail too.
    "10.2_Appendix_Tool Use.ipynb": {
        15: "ValueError",
        17: "NameError",
        19: "NameError",
        41: "ValueError",
        42: "NameError",
        43: "NameError",
    },
}


@pytest.fixture(scope="module")
def ipython_home(tmp_path_factory):
    """A throwaway HOME so ``%store`` writes to a temp IPython profile, not the user's."""
    return tmp_path_factory.mktemp("home")


@pytest.mark.slow
def test_first_party_notebooks_execute_offline(ipython_home, monkeypatch):
    nbclient = pytest.importorskip("nbclient")

    monkeypatch.setenv("HOME", str(ipython_home))
    monkeypatch.setenv("PYTHONPATH", os.pathsep.join([str(STUBS), os.environ.get("PYTHONPATH", "")]))
    monkeypatch.setenv("ANTHROPIC_API_KEY", "offline-test-placeholder")

    failures = []
    # 00 must run first: it stores API_KEY and MODEL_NAME for the other notebooks.
    for path in FIRST_PARTY_NOTEBOOKS:
        nb = nbformat.read(path, as_version=4)
        for _, cell in _code_cells(nb):
            # Skip the package install line; the stub stands in for the SDK.
            cell.source = "\n".join(
                line for line in cell.source.splitlines() if not line.lstrip().startswith(("%pip", "!pip"))
            )
        client = nbclient.NotebookClient(
            nb,
            timeout=120,
            allow_errors=True,
            kernel_name="python3",
            resources={"metadata": {"path": str(FIRST_PARTY)}},
        )
        client.execute()

        expected = EXPECTED_ERRORS.get(path.name, {})
        seen = {}
        for index, cell in _code_cells(nb):
            for output in cell.outputs:
                if output.output_type == "error":
                    seen[index] = output.ename
        if seen != expected:
            failures.append(f"{path.name}: expected errors {expected}, got {seen}")

    assert not failures, "\n".join(failures)


if __name__ == "__main__":  # pragma: no cover
    sys.exit(pytest.main([__file__, "-v"]))
