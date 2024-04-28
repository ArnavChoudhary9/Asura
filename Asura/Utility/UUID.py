from uuid import UUID, uuid3, uuid4, NAMESPACE_URL
from typing import Callable

UUID3Generator: Callable[[str], UUID] = lambda asset: uuid3(NAMESPACE_URL, asset)
UUID4Generator: Callable[[], UUID] = lambda: uuid4()
