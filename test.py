from modules.class_peer_group import peer_group


def unittest():
    peergroup = peer_group()
    list_test = peergroup.add_company("AAPL")
    assert type(list_test) == list


if __name__ == "__main__":
    unittest()
