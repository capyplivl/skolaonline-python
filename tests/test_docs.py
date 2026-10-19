from __future__ import annotations

import ast
import inspect
from pathlib import Path

from skolaonline import SkolaOnline
from skolaonline.resources._base import SyncAPIResource
from tests._helpers import public_methods

PACKAGE = Path(__file__).parent.parent / "src" / "skolaonline"


def _is_docstring(node: ast.stmt | None) -> bool:
    return (
        isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Constant)
        and isinstance(node.value.value, str)
    )


def _undocumented(body: list[ast.stmt], prefix: str, path: Path) -> list[str]:
    missing = []
    for index, node in enumerate(body):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            if node.name.startswith("_"):
                continue
            if ast.get_docstring(node) is None:
                missing.append(f"{path.name}:{node.lineno} {prefix}{node.name}")
            if isinstance(node, ast.ClassDef):
                missing += _undocumented(node.body, f"{prefix}{node.name}.", path)
        elif prefix and isinstance(node, ast.AnnAssign | ast.Assign):
            target = node.target if isinstance(node, ast.AnnAssign) else node.targets[0]
            if isinstance(target, ast.Name) and not target.id.startswith("_"):
                following = body[index + 1] if index + 1 < len(body) else None
                if not _is_docstring(following):
                    missing.append(f"{path.name}:{node.lineno} {prefix}{target.id}")
    return missing


def test_public_api_is_documented() -> None:
    missing = []
    for path in sorted(PACKAGE.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        missing += _undocumented(tree.body, "", path)
    assert missing == []


def test_method_docstrings_describe_every_parameter() -> None:
    client = SkolaOnline(access_token="token")
    problems = []
    for resource_name, resource in vars(client).items():
        if not isinstance(resource, SyncAPIResource):
            continue
        for method_name, method in public_methods(resource):
            doc = inspect.getdoc(method) or ""
            for name in inspect.signature(method).parameters:
                if f"\n    {name}: " not in doc:
                    problems.append(f"{resource_name}.{method_name}({name})")
    assert problems == []
