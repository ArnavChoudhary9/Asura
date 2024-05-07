class Math:
    @staticmethod
    def PythonInt32ToBytes ( value: int   , byteorder='big' ) -> bytes : return value.to_bytes(4, byteorder) # type: ignore
    @staticmethod
    def BytesToPythonInt32 ( value: bytes , byteorder='big' ) -> int   : return int.from_bytes(value, byteorder) # type: ignore
