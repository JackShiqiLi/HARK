import HARK.ConsumptionSaving.ConsPortfolioFrameModel as cpfm
import numpy as np
import unittest


class PortfolioConsumerTypeTestCase(unittest.TestCase):
    def setUp(self):
        # Create portfolio choice consumer type
        self.pcct = cpfm.PortfolioConsumerFrameType()
        self.pcct.cycles = 0

        # Solve the model under the given parameters

        self.pcct.solve()

class UnitsPortfolioConsumerTypeTestCase(PortfolioConsumerTypeTestCase):
    def test_simOnePeriod(self):

        self.pcct.T_sim = 30
        self.pcct.AgentCount = 10
        self.pcct.track_vars += ['aNrm']
        self.pcct.initialize_sim()

        self.assertFalse(
            np.any(self.pcct.shocks['Adjust'])
        )

        self.pcct.sim_one_period()

        self.assertAlmostEqual(
            self.pcct.shocks['PermShk'][0],
            0.9692322
        )

        self.assertAlmostEqual(
            self.pcct.shocks['TranShk'][0],
            1.03172631
        )

        self.assertAlmostEqual(
             self.pcct.aggs['Risky'][0],
             0.96358739
        )

        self.assertAlmostEqual(
            self.pcct.state_now['pLvl'][0],
            self.pcct.state_prev['pLvl'][0] * self.pcct.shocks['PermShk'][0]
        )

        self.assertTrue(
            np.any(self.pcct.shocks['Adjust'][0])
        )

        self.assertAlmostEqual(
            self.pcct.state_now["mNrm"][0],
            self.pcct.state_prev["aNrm"][0] \
            * self.pcct.Rfree / self.pcct.shocks['PermShk'][0] \
            + self.pcct.shocks['TranShk'][0] \
        )

        self.assertAlmostEqual(
            # todo: more flexible test
            self.pcct.controls["Share"][0],
            0.90256316
        )
        self.assertAlmostEqual(
            self.pcct.controls["cNrm"][0],
            self.pcct.solution[0].cFuncAdj(self.pcct.state_now['mNrm'][0])
        )

        self.assertAlmostEqual(
            self.pcct.state_now['aNrm'][0],
            self.pcct.state_now["mNrm"][0] - self.pcct.controls["cNrm"][0]
        )

class SimulatePortfolioConsumerTypeTestCase(PortfolioConsumerTypeTestCase):

    def test_simulation(self):

        self.pcct.T_sim = 30
        self.pcct.AgentCount = 10
        self.pcct.track_vars += [
            'mNrm',
            'cNrm',
            'Share',
            'aNrm',
            'Adjust',
            'PermShk',
            'TranShk',
            'bNrm'
        ]
        self.pcct.initialize_sim()

        self.pcct.simulate()

        self.assertAlmostEqual(
            self.pcct.history["mNrm"][0][0],
            self.pcct.history["bNrm"][0][0] \
            + self.pcct.history['TranShk'][0][0]
        )

        self.assertAlmostEqual(
            self.pcct.history['cNrm'][0][0],
            self.pcct.solution[0].cFuncAdj(self.pcct.history['mNrm'][0][0])
        )

        self.assertAlmostEqual(
            self.pcct.history['Share'][0][0],
            self.pcct.solution[0].ShareFuncAdj(self.pcct.history['mNrm'][0][0])
        )

        self.assertAlmostEqual(
            self.pcct.history['aNrm'][0][0],
            self.pcct.history["mNrm"][0][0] - self.pcct.history["cNrm"][0][0]
        )

        self.assertAlmostEqual(
            self.pcct.history['Adjust'][0][0], 1.0
        )
        # the next period

        self.assertAlmostEqual(
            self.pcct.history["mNrm"][1][0],
            self.pcct.history["bNrm"][1][0] \
            + self.pcct.history['TranShk'][1][0]
        )

        self.assertAlmostEqual(
            self.pcct.history['cNrm'][1][0],
            self.pcct.solution[0].cFuncAdj(self.pcct.history['mNrm'][1][0])
        )

        self.assertAlmostEqual(
            self.pcct.history['Share'][1][0],
            self.pcct.solution[0].ShareFuncAdj(self.pcct.history['mNrm'][1][0])
        )

        self.assertAlmostEqual(
            self.pcct.history['aNrm'][1][0],
            self.pcct.history["mNrm"][1][0] - self.pcct.history["cNrm"][1][0]
        )

        self.assertAlmostEqual(
            self.pcct.history['aNrm'][15][0],
            self.pcct.history["mNrm"][15][0] - self.pcct.history["cNrm"][15][0]
        )
