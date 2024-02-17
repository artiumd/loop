from typing import Iterator, Callable, Any, Optional, Union
from contextlib import contextmanager

from tqdm import tqdm


@contextmanager
def dummy_progress() -> Iterator[Callable[[Any], None]]:
    yield lambda *args, **kwargs: None


class TqdmProgbar:
    def __init__(self, refresh: bool, postfix_str: Optional[Union[str, Callable[[Any], Any]]] = None, **kwargs):
        self._on_set_postfix = self._do_nothing
        self._on_refresh = self._do_nothing
        self._tqdm = tqdm(**kwargs)
        self._refresh = refresh

        if isinstance(postfix_str, str):
            self._tqdm.set_postfix_str(postfix_str)
        elif callable(postfix_str):
            self._postfix_str = postfix_str
            self._on_set_postfix = self._do_set_postfix

        if refresh:
            self._on_refresh = self._do_refresh

    def __enter__(self):
        self._tqdm.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._tqdm.__exit__(exc_type, exc_val, exc_tb)

    def __call__(self, retval: Any) -> None:
        self._tqdm.update()
        self._on_set_postfix(retval)
        self._on_refresh()

    def _do_nothing(self, *args, **kwargs) -> None:
        pass

    def _do_set_postfix(self, retval: Any) -> None:
        postfix_str = str(self._postfix_str(retval))
        self._tqdm.set_postfix_str(postfix_str, refresh=False)  # `self._tqdm.refresh()` will be called separately if constructed with `refresh=True`.

    def _do_refresh(self) -> None:
        self._tqdm.refresh()
