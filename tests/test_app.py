import pandas as pd
import app.app

test_data_der = [{'portfolio': [1, 2], 'risk': [3, 4]}]
test_data_fx = [{'portfolio': [3, 4], 'risk': [5, 6]}]
test_data_cash = pd.DataFrame({'portfolio': [5, 6], 'risk': [-7, -8]})
test_data_risks = pd.DataFrame({'portfolio': [1, 2, 3, 4, 5, 6], 'risk': [3, 4, 5, 6, -7, -8]})


# def test_get_risks_mocked(mocker):
#     mocker.patch.object(app.app.get_risks, 'risk_value_der', test_data_der)
#     mocker.patch.object(app.app.get_risks, 'risk_value_fx', test_data_fx)
#     mocker.patch.object(app.app.get_risks, 'cashrisks', test_data_cash)
#
#     expected = test_data_risks
#     actual = app.app.get_risks()
#
#     assert expected == actual

def test_main_mocked(mocker):
    #mocker.patch.object(app.app.main.read_portfolio_data, 'portfolio', test_data_der)
    #mocker.patch.object(app.app.main.read_cashrisks_data, 'cashrisks', test_data_cash)
    mocker.patch('app.app.main.get_risks', test_data_risks)
    #mocker.patch.object(app.app.get_risks, 'cashrisks', test_data_cash)

    expected = test_data_risks
    actual = app.app.get_risks()

    assert expected == actual

# import unittest
#
#
# class MyTestCase(unittest.TestCase):
#     def test_something(self):
#         self.assertEqual(True, False)
#
#
# if __name__ == '__main__':
#     unittest.main()
