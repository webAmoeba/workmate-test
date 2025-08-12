import importlib
import pkgutil

import workmate.reports as reports_pkg


def discover_reports() -> dict[str, callable]:
    """Searches all modules in workmate.reports
    with function make_report(records)."""
    discovered: dict[str, callable] = {}

    for _, module_name, _ in pkgutil.iter_modules(reports_pkg.__path__):
        mod = importlib.import_module(f"{reports_pkg.__name__}.{module_name}")
        fn = getattr(mod, "make_report", None)
        if callable(fn):
            discovered[module_name] = fn

            for alias in getattr(mod, "ALIASES", []):
                discovered.setdefault(alias, fn)
    return discovered