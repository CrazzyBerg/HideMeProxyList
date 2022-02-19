import unittest
from HideME import HideME


class HideMeTest(unittest.TestCase):

    def test_count_param_with_two(self):
        proxy = HideME(url='/proxy-list/', count=2)
        proxies = len(proxy.get())
        self.assertGreaterEqual(proxies, 2, "Count filter for 2 proxies failed.")

    def test_count_param_with_twenty(self):
        proxy = HideME(url='/proxy-list/', count=20)
        proxies = len(proxy.get())
        self.assertGreaterEqual(proxies, 20, "Count filter for 20 proxies failed.")

    def test_no_count_value_passed(self):
        proxy = HideME(url='/proxy-list/')
        proxies = proxy.get()
        self.assertGreaterEqual(len(proxies), 512, "Greater than proxies were not returned")


def suite():
    suite = unittest.TestSuite()
    suite.addTest(HideMeTest('test_count_param_with_two'))
    suite.addTest(HideMeTest('test_count_param_with_twenty'))
    suite.addTest(HideMeTest('test_no_count_value_passed'))

    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())