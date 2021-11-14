from warnings import resetwarnings
import pytest

from utils.text_preparation import get_filtered_context


@pytest.mark.parametrize("replica,", [
    'test123',
    'Hello world test',
    '1 2 3 4 5 6 7 8 9',
    '1 2 3 4 5 6 7 8 9 10',
    '',
    '        ',
])
def test_context_filtering_words(replica):
    user_replicas = [replica for i in range(1000)]

    tokens_count = len(replica.split(' '))
    filters_replicas = get_filtered_context(user_replicas)

    excepted = 100 // tokens_count + bool(100 % tokens_count)

    if replica.strip():
        assert len(filters_replicas) ==  excepted
        assert len(filters_replicas[-1].split(' ')) == (100 % tokens_count or tokens_count)
    else:
        assert len(filters_replicas) == 0

