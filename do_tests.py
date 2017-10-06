from unittest import TestSuite, TextTestRunner, TestLoader
import test_events
import test_cfg
import test_entities
import test_context
import test_input
import test_controller


def make_suite():
    loader = TestLoader()
    suite = TestSuite()

    suite.addTests(loader.loadTestsFromModule(test_events))
    suite.addTests(loader.loadTestsFromModule(test_cfg))
    suite.addTests(loader.loadTestsFromModule(test_entities))
    suite.addTests(loader.loadTestsFromModule(test_context))
    suite.addTests(loader.loadTestsFromModule(test_input))
    suite.addTests(loader.loadTestsFromModule(test_controller))

    return suite

if __name__ == "__main__":
    runner = TextTestRunner(verbosity=3)
    runner.run(make_suite())

