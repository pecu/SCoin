class Bundle():
    def __init__(self, hash=None):
        if hash == None:
            hash = "RUBXZTNOIYV9EULYYHKEEAHFFQPYMPZIXLVYNPHGBDBDDZERDSJHJAMGOIHHGILZGDYNP9ANJANPHZYDX"
        self.hash = hash

class IotaMock():
    def __init__(self, node_url, seed=None):
        self.url = node_url
        self.seed = seed

    def send_transfer(self, depth, transfers, min_weight_magnitude):
        return {
            "bundle": Bundle()
        }

    def find_transactions(self, bundles):
        if bundles == ["RUBXZTNOIYV9EULYYHKEEAHFFQPYMPZIXLVYNPHGBDBDDZERDSJHJAMGOIHHGILZGDYNP9ANJANPHZYDX"]:
            return { "hashes": ["KYVEAQJKIYSNH9SGULNSPDFGULCV9DETKWIFUUH9GICWMMYJFRVUSDWFNXIAXBHW9BNNXOKGVOMKZ9999"] }

def iota_mock(node_url, seed=None):
    return IotaMock(node_url, seed)
