from modules.class_peer_group import Peer_Group
import pytest
import pandas as pd


def test_peer_group_index():
    assert Peer_Group().index == "test_index"
