import pytest
from unittest.mock import patch, ANY 

from main import setup


def test_setup():
    with patch('main.setup_logging') as m_setup_logging:
        setup()
        m_setup_logging.assert_called_once()
