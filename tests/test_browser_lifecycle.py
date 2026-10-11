"""A manually closed demo tab must not prevent starting a new run."""

from unittest.mock import Mock

import pytest

from jev_ultrafast import browser


def test_close_accepts_an_already_closed_tab(monkeypatch):
    tab = browser.Browser.__new__(browser.Browser)
    tab.target = "closed-tab"
    cdp = Mock(side_effect=RuntimeError("{'code': -32602, 'message': 'No target with given id found'}"))
    monkeypatch.setattr(browser, "cdp", cdp)
    tab.close()
    tab.close()
    assert tab.target is None
    cdp.assert_called_once_with("Target.closeTarget", targetId="closed-tab")


def test_close_does_not_hide_transport_errors(monkeypatch):
    tab = browser.Browser.__new__(browser.Browser)
    tab.target = "owned-tab"
    monkeypatch.setattr(browser, "cdp", Mock(side_effect=RuntimeError("Connection lost")))
    with pytest.raises(RuntimeError, match="Connection lost"):
        tab.close()
    assert tab.target == "owned-tab"


def test_show_closed_tab_explains_how_to_recover(monkeypatch):
    tab = browser.Browser.__new__(browser.Browser)
    tab.target = "closed-tab"
    monkeypatch.setattr(browser, "cdp", Mock(side_effect=RuntimeError("No target with given id found")))
    with pytest.raises(ValueError, match="Click Start demo"):
        tab.show()
