import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(ROOT, 'Automation'))

from compliance_checker import calculate_iso_compliance, calculate_nist_compliance
from risk_analyzer import calculate_risk_summary, identify_risks_above_appetite


class DashboardLogicTests(unittest.TestCase):
    def test_nist_score_is_percentage_of_controls_meeting_target(self):
        data = [
            {'Included in Profile?': 'Yes', 'Current Status': 2.0, 'Target Maturity (1-4)': 3.0, 'Gap (Y/N)': 'Y', 'Priority (High/Medium/Low)': 'Medium'},
            {'Included in Profile?': 'Yes', 'Current Status': 3.0, 'Target Maturity (1-4)': 3.0, 'Gap (Y/N)': 'N', 'Priority (High/Medium/Low)': 'Low'},
            {'Included in Profile?': 'No', 'Current Status': 3.0, 'Target Maturity (1-4)': 3.0, 'Gap (Y/N)': 'N', 'Priority (High/Medium/Low)': 'Low'},
        ]
        score, gaps, high, top = calculate_nist_compliance(data)
        self.assertEqual(score, 50.0)
        self.assertEqual(gaps, 1)
        self.assertEqual(high, 0)
        self.assertEqual(len(top), 1)

    def test_iso_score_counts_only_applicable_controls(self):
        data = [
            {'Applicable (Yes/No)': 'Yes', 'Implementation Status': 'Implemented'},
            {'Applicable (Yes/No)': 'Yes', 'Implementation Status': 'Partial'},
            {'Applicable (Yes/No)': 'Yes', 'Implementation Status': 'Not Implemented'},
            {'Applicable (Yes/No)': 'No', 'Implementation Status': 'Implemented'},
        ]
        score, missing = calculate_iso_compliance(data)
        self.assertEqual(score, 33.3)
        self.assertEqual(missing, 2)

    def test_risk_summary_flags_scores_above_appetite(self):
        data = [
            {'Risk ID': 'R-001', 'Likelihood (1-5)': 3, 'Impact (1-5)': 5},
            {'Risk ID': 'R-002', 'Likelihood (1-5)': 2, 'Impact (1-5)': 4},
            {'Risk ID': 'R-003', 'Likelihood (1-5)': 4, 'Impact (1-5)': 5},
        ]
        summary = calculate_risk_summary(data)
        self.assertEqual(summary['R-001']['score'], 15)
        self.assertEqual(summary['R-003']['risk_level'], 'Critical')
        self.assertEqual(len(identify_risks_above_appetite(summary)), 2)


if __name__ == '__main__':
    unittest.main()
