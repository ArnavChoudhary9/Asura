class Layer:
    __slots__ = "_Name", "_Enabled"
    _Name: str
    _Enabled: bool

    def __init__(self, name: str="Layer") -> None:
        self._Name = name
        self._Enabled = True
        self.OnInitialize()
    
    def OnInitialize(self) -> None: ...
