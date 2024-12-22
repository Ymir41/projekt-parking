import unittest

from src.Signal import Signal

class TestSignal(unittest.TestCase):

    def test_add_slot(self):
        signal = Signal()
        def dummy_function():
            pass
        signal.addSlot(dummy_function)
        self.assertIn(dummy_function, signal.slots)

    def test_emit_no_args(self):
        signal = Signal()
        self.called = False

        def slot():
            self.called = True
        
        signal.addSlot(slot)
        signal.emit()

        self.assertTrue(self.called)

    def test_emit_with_args(self):
        signal = Signal()
        self.result = None

        def slot(arg1, arg2):
            self.result = arg1 + arg2

        signal.addSlot(slot)
        signal.emit(2, 3)

        self.assertEqual(self.result, 5)

    def test_emit_multiple_slots(self):
        signal = Signal()
        self.calls = []

        def slot1():
            self.calls.append('slot1')

        def slot2():
            self.calls.append('slot2')

        signal.addSlot(slot1)
        signal.addSlot(slot2)
        signal.emit()

        self.assertEqual(self.calls, ['slot1', 'slot2'])


if __name__ == "__main__":
    unittest.main()
