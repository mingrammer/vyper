

def test_map_delete(get_contract_with_gas_estimation):
    code = """
big_storage: bytes32[bytes32]

@public
def set(key: bytes32, value: bytes32):
    self.big_storage[key] = value

@public
def get(key: bytes32) -> bytes32:
    return self.big_storage[key]

@public
def delete(key: bytes32):
    del self.big_storage[key]
    """

    c = get_contract_with_gas_estimation(code)

    assert c.get("test") == b'\x00' * 32
    c.set("test", "value")
    assert c.get("test")[:5] == b"value"
    c.delete("test")
    assert c.get("test") == b'\x00' * 32


def test_map_delete_nested(get_contract_with_gas_estimation):
    code = """
big_storage: bytes32[bytes32][bytes32]

@public
def set(key1: bytes32, key2: bytes32, value: bytes32):
    self.big_storage[key1][key2] = value

@public
def get(key1: bytes32, key2: bytes32) -> bytes32:
    return self.big_storage[key1][key2]

@public
def delete(key1: bytes32, key2: bytes32):
    del self.big_storage[key1][key2]
    """

    c = get_contract_with_gas_estimation(code)

    assert c.get("test1", "test2") == b'\x00' * 32
    c.set("test1", "test2", "value")
    assert c.get("test1", "test2")[:5] == b"value"
    c.delete("test1", "test2")
    assert c.get("test1", "test2") == b'\x00' * 32


def test_map_delete_struct(get_contract_with_gas_estimation):
    code = """
structmap: {
    a: int128,
    b: int128
}[int128]


@public
def set():
    self.structmap[123] = {
        a: 333,
        b: 444
    }

@public
def get() -> (int128, int128):
    return self.structmap[123].a, self.structmap[123].b

@public
def delete():
    self.structmap[123] = None
    """

    c = get_contract_with_gas_estimation(code)

    assert c.get() == [0, 0]
    c.set()
    assert c.get() == [333, 444]
    c.delete()
    assert c.get() == [0, 0]
