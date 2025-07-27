import os
from pathlib import Path

from dotenv import load_dotenv
from invoke import Collection, Context, task

# load .env from project root
project_root = Path(__file__).parent
load_dotenv(project_root / ".env")
LINT_PATHS = os.getenv("LINT_PATHS", ". ./tests").split()
LINE_LENGTH: int = 95


@task  # type: ignore[misc]
def bandit(c: Context) -> None:
    """
    Run Bandit security scan over your source.

    Usage: invoke bandit
    """
    c.run("poetry run bandit -r src/helloworld -c bandit.yml", pty=True)


@task(help={"level": "Which part to bump: patch, minor, or major"})  # type: ignore[misc]
def bump(c: Context, level: str = "patch") -> None:
    """
    Bump version with Poetry, commit, tag, and push to GitHub.

    Usage:
      invoke release          # patch bump
      invoke release --level=minor
      invoke release --level=major
    """
    # 1) bump version in pyproject.toml
    result = c.run(f"poetry version {level}", hide="both")
    new_version = result.stdout.strip()

    # 2) stage all changes
    c.run("git add .", pty=True)

    # 3) commit with conventional message
    c.run(f'git commit -m "chore(release): bump version to {new_version}"', pty=True)

    # 4) create the Git tag
    c.run(f"git tag v{new_version}", pty=True)

    # 5) push the tag only
    c.run(f"git push origin v{new_version}", pty=True)

    # 6) push commit and any remaining tags
    c.run("git push --follow-tags", pty=True)


@task  # type: ignore[misc]
def docs(c: Context) -> None:
    """
    Build the MkDocs site locally.

    Usage: invoke docs
    """
    c.run("poetry run mkdocs build --config-file ./docs/mkdocs.yml", pty=True)


@task  # type: ignore[misc]
def docs_serve(c: Context) -> None:
    """
    Serve MkDocs locally with live reload.

    Usage: invoke docs-serve
    """
    c.run("poetry run mkdocs serve --config-file ./docs/mkdocs.yml", pty=True)


@task  # type: ignore[misc]
def docstyle(c: Context) -> None:
    """
    Run pydocstyle to enforce docstring conventions.

    Usage: invoke docstyle
    """
    # point at your source (and tests if you like)
    c.run("poetry run pydocstyle src/helloworld tests", pty=True)


@task  # type: ignore[misc]
def fmt(c: Context) -> None:
    """
    Auto‑format code: reorder imports with isort and apply Black formatting.

    Usage: invoke fmt
    """
    # reorder imports in place
    c.run("poetry run isort .", pty=True)
    # format code with Black
    c.run("poetry run black .", pty=True)


@task  # type: ignore[misc]
def lint(c: Context) -> None:
    """
    Run all lint checks: Black, isort, and Flake8 (ignoring E501).

    Usage: poetry run invoke lint
    """
    # join back into a single string for CLI calls
    paths_arg = " ".join(LINT_PATHS)

    # Black in check-only mode
    c.run(f"poetry run black --check {paths_arg}", pty=True)

    # isort in check-only mode
    c.run(f"poetry run isort --check {paths_arg}", pty=True)

    # flake8 ignoring line-too-long errors
    c.run(f"poetry run flake8 {paths_arg} --ignore=E501", pty=True)a


@task  # type: ignore[misc]
def sync(c: Context) -> None:
    """
    Fully sync local main branch to origin/main, discarding all local changes.

    Usage: invoke sync
    """
    # ensure we’re on main
    c.run("git checkout main", pty=True)
    # fetch + prune deleted remotes
    c.run("git fetch origin --prune", pty=True)
    # hard reset to remote state
    c.run("git reset --hard origin/main", pty=True)
    # remove untracked files and dirs
    c.run("git clean -fd", pty=True)


@task  # type: ignore[misc]
def test(c: Context) -> None:
    """
    Run the full pytest suite.

    Usage: invoke test
    """
    c.run("poetry run pytest", pty=True)


@task  # type: ignore[misc]
def typecheck(c: Context) -> None:
    """
    Run MyPy static type checks.

    Usage: invoke typecheck
    """
    # Point at your source package directory (adjust as needed)
    c.run("poetry run mypy src/helloworld tests", pty=True)


# Create a namespace and add tasks
ns = Collection()
ns.add_task(bandit)
ns.add_task(bump)
ns.add_task(docs)
ns.add_task(docs_serve)
ns.add_task(docstyle)
ns.add_task(fmt)
ns.add_task(lint)
ns.add_task(sync)
ns.add_task(test)
ns.add_task(typecheck)


@task(
    pre=[fmt, lint, typecheck, docstyle, test, bandit, docs],
)  # type: ignore[misc]
def ci(c: Context) -> None:
    """
    Run all CI tasks in order: fmt, lint, typecheck, docstyle, test, bandit.

    Usage: invoke ci
    """
    print("🎉 All CI tasks completed successfully!")


ns.add_task(ci)


@task(default=True)  # type: ignore[misc]
def help(c: Context) -> None:
    """
    Show available tasks.

    Usage: invoke help
    """
    print("Available tasks:\n")
    for name, task_obj in ns.tasks.items():
        print(f"  {name:10} — {task_obj.__doc__.strip()}")


ns.add_task(help)