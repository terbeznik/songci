import songci


def test_free_proxy_list_net():
    proxies = songci.free_proxy_list_net()

    assert len(proxies) > 200


def test_spys_me():
    proxies = songci.spys_me()

    assert len(proxies) > 200


def test_proxy_daily_com():
    proxies = songci.proxy_daily_com()

    assert len(proxies) > 1000


def test_proxyscrape_com():
    proxies = songci.proxyscrape_com()
    print(len(proxies))
    assert len(proxies) > 1000
