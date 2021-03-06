from text_processors.chunk import OverlappingFixedSizeChunk
from text_processors.split import WhiteSpaceSplit


def test_white_space_split():
    text = "hello i am a robot"
    wss = WhiteSpaceSplit()
    assert wss(text) == text.split()


def test_chunk():
    text = "hello i am a robot"
    wss = WhiteSpaceSplit()
    assert wss(text) == text.split()
    ofsc = OverlappingFixedSizeChunk(3, 1)
    assert list(ofsc(wss(text))) == [['hello', 'i', 'am'], ['am', 'a', 'robot'], ['robot']]