"""
This module creates the class to couple GEMMES and MATER models.
"""

import time as t
import pandas as pd
import numpy as np
from mater_package import MATER
from mater_package.mater_func import concat_


class GemmesMater(MATER):
    """Uses the MATER model to analyse a GEMMES model run."""

    '''def Impact_variables_definition(self):
        """Defines the impact variables."""
        self.ImpactEnergy = pd.DataFrame(
            data=0,
            index=pd.MultiIndex.from_product(
                [
                    self.vector["Approach"],
                    self.vector["Calcul"],
                    self.vector["Region"],
                    self.vector["Impact"],
                ],
                names=["Approach", "Calcul", "Region", "Impact"],
            ),
            columns=self.LifeTimeMeanValue.columns,
        )

        self.ImpactResources = pd.DataFrame(
            data=0,
            index=pd.MultiIndex.from_product(
                [
                    self.vector["Approach"],
                    self.vector["Calcul"],
                    self.vector["Region"],
                    self.vector["Impact"],
                ],
                names=["Approach", "Calcul", "Region", "Impact"],
            ),
            columns=self.LifeTimeMeanValue.columns,
        )

        self.ImpactTotal = pd.DataFrame(
            data=0,
            index=pd.MultiIndex.from_product(
                [
                    self.vector["Approach"],
                    self.vector["Calcul"],
                    self.vector["Region"],
                    self.vector["Impact"],
                ],
                names=["Approach", "Calcul", "Region", "Impact"],
            ),
            columns=self.LifeTimeMeanValue.columns,
        )'''

    def stock_computation_energy_stock_start(self):
        """Computes the TU stocks of transport without ships and building sectors.

        Input attributes
        ----------------
        vector : dict
            Dictionary of mapping vectors
        EnergyDemand : DataFrame
            Energy demand by TU [J/year]
        TUTransportEnergyConsumption : DataFrame
            Vehicles energy consumption [J/km]
        TUTransportIntensityOfUse : DataFrame
            Vehicles intensity of use [km/year/vehicle]
        TUBuildingTUIndustryEnergyConsumption : DataFrame
            Buildings energy consumption [J/building unit]
        TUStockScenario : DataFrame
            Scenario stocks for each TU [TU]
        TUStockShareScenario : DataFrame
            Scenario stock shares for each vehicle type [TU/TU]

        Output attributes
        ----------------
        TUStock : DataFrame
            Number of TU in the society [TU]

        Notes
        -----
        Energy start :
            Transport sector :
        .. math:: \text{Stock [TU]} = \frac{\text{Energy demand [J/year]}}{\text{Consumption [J/km]}\times\text{Intensity of use [km/TU/year]}
        """
        self.TUStock.loc[["EnergyStart"], :, :, self.vector["TUTransport"], :] = concat_(
            ["EnergyStart"],
            "Approach",
            self.vector["CalculAll"],
            "Calcul",
            self.EnergyDemand.loc[:, self.vector["TUTransport"], :]
            .div(self.TUTransportEnergyConsumption)
            .div(self.TUTransportIntensityOfUse),
        )

        self.TUStock.loc[["EnergyStart"], :, :, self.vector["TUBuilding"], :] = concat_(
            ["EnergyStart"],
            "Approach",
            self.vector["CalculAll"],
            "Calcul",
            self.EnergyDemand.loc[:, self.vector["TUBuilding"], :].div(self.TUBuildingTUIndustryEnergyConsumption),
        )

        '''self.TUStock.loc[["StockStart"], :, :, self.vector["TUTransportWithoutShip"], :] = concat_(
            ["StockStart"],
            "Approach",
            self.vector["CalculAll"],
            "Calcul",
            self.TUStockScenario.loc[:, self.vector["TUTransportWithoutShip"], :].mul(
                self.TUStockShareScenario.loc[:, self.vector["TUTransportWithoutShip"], :]
            ),
        )'''

        self.TUStock = self.TUStock.loc[self.vector["Approach"], self.vector["Calcul"], :, :, :]

    def stock_computation_logistical_start_battery_tire(self, i: int):
        """Computes the TU stocks of transport without ships and building sectors.

        Input attributes
        ----------------
        vector : dict
            Dictionary of mapping vectors
        TUStockLogistic : DataFrame
            Logistic parameters for the TU stocks
        TUStockShareLogisticTime : DataFrame
            Logistic stock shares for each vehicle type [TU/TU]
        Population : DataFrame
            Population from 1900 to 2100 [capita]
        GDPperCapita : DataFrame
            GDP per capita from 1900 to 2100 [$ppp constant]

        Output attributes
        ----------------
        TUStock : DataFrame
            Number of TU in the society [TU]

        Notes
        -----
        Energy start :
            Transport sector :
        .. math:: \text{Stock [TU]} = \frac{\text{Energy demand [J/year]}}{\text{Consumption [J/km]}\times\text{Intensity of use [km/TU/year]}
        """

        TULogistic = (
            self.GDPperCapita[i]
            .sub(
                self.TUStockLogistic["x Initial"],
                axis=0,
            )
            .mul(
                -self.TUStockLogistic["C"],
                axis=0,
            )
            .astype(float)
            .apply(np.exp)
            .mul(-self.TUStockLogistic["B"], axis=0)
            .astype(float)
            .apply(np.exp)
            .mul(
                self.TUStockLogistic["Saturation Value"],
                axis=0,
            )
            .mul(
                self.Population[i],
                axis=0,
            )
            .apply(lambda col: pd.to_numeric(col, errors="coerce"))
        )

        '''self.TUStock[i].loc[["LogisticalStart"], ["Endogenous"], :, self.vector["TUTransportWithoutShip"],] = concat_(
            ["LogisticalStart"],
            "Approach",
            ["Endogenous"],
            "Calcul",
            TULogistic.mul(self.TUStockShareLogisticTime[i], axis=0),
        )'''

        self.TUStock[i].loc[:, :, :, self.vector["TUTransportBattery"]] = (
            self.TUStock[i]
            .loc[:, :, :, self.vector["TUTransportRoad"]]
            .rename(
                index=dict(
                    zip(
                        np.ravel(
                            [self.vector["TUTransportRoad"]]
                            * len(self.vector["Approach"])
                            * len(self.vector["Calcul"])
                            * len(self.vector["Region"])
                        ),
                        np.ravel(
                            [self.vector["TUTransportBattery"]]
                            * len(self.vector["Approach"])
                            * len(self.vector["Calcul"])
                            * len(self.vector["Region"])
                        ),
                    )
                ),
                level="TU",
            )
        )

        self.TUStock[i].loc[:, :, :, self.vector["TUTransportTire"]] = (
            self.TUStock[i]
            .loc[:, :, :, self.vector["TUTransportRoad"]]
            .rename(
                index=dict(
                    zip(
                        np.ravel(
                            [self.vector["TUTransportRoad"]]
                            * len(self.vector["Approach"])
                            * len(self.vector["Calcul"])
                            * len(self.vector["Region"])
                        ),
                        np.ravel(
                            [self.vector["TUTransportTire"]]
                            * len(self.vector["Approach"])
                            * len(self.vector["Calcul"])
                            * len(self.vector["Region"])
                        ),
                    )
                ),
                level="TU",
            )
            .mul(self.TUTireInRoad[i])
        )

    def energy_demand_computation_energy_stock_start(self):
        """Computes the energy demand of transport without ships and building sectors.

        Input attributes
        ----------------
        vector : dict
            Dictionary of mapping vectors
        EnergyDemand : DataFrame
            Energy demand by TU [J/year]

        Output attributes
        ----------------
        EnergyDemandFinalTUDemand : DataFrame
            Total energy demand for the transport, building and industrial sectors [J/year]

        Notes
        -----
        Stock start :
            Transport sector :
        .. math:: \text{Energy demand [J/year]} = \text{Stock [TU]}\times\text{Consumption [J/km]}\times\text{Intensity of use [km/TU/year]}
        """
        self.EnergyDemandFinalTUDemand.loc[["EnergyStart"], :, :, self.vector["TUEnergyDemand"], :] = concat_(
            ["EnergyStart"],
            "Approach",
            self.vector["CalculAll"],
            "Calcul",
            self.EnergyDemand.loc[:, self.vector["TUEnergyDemand"], :],
        )

        self.EnergyDemandFinalTUDemand.loc[["EnergyStart"], ["Endogenous"], :, self.vector["TUIndustry"], :] = 0

        self.EnergyDemandFinalTUDemand.loc[["StockStart"], :, :, self.vector["TUTransport"], :] = self.TUStock.loc[
            ["StockStart"], :, :, self.vector["TUTransport"], :
        ].mul(
            concat_(
                ["StockStart"],
                "Approach",
                self.vector["CalculAll"],
                "Calcul",
                self.TUTransportEnergyConsumption.mul(self.TUTransportIntensityOfUse),
            ),
            axis=0,
        )

        self.EnergyDemandFinalTUDemand.loc[["StockStart"], :, :, self.vector["TUBuilding"], :] = self.TUStock.loc[
            ["StockStart"], :, :, self.vector["TUBuilding"], :
        ].mul(
            concat_(
                ["StockStart"],
                "Approach",
                self.vector["CalculAll"],
                "Calcul",
                self.TUBuildingTUIndustryEnergyConsumption,
            ),
            axis=0,
        )

        self.EnergyDemandFinalTUDemand.drop("Endogenous", axis=1, inplace=True)

        self.EnergyDemandFinalTUDemand = self.EnergyDemandFinalTUDemand.loc[
            self.vector["Approach"], self.vector["Calcul"], :, :, :
        ]

    def energy_demand_computation_logistical_start(self, i: int):
        """Computes the energy demand of transport without ships and building sectors.

        Input attributes
        ----------------
        vector : dict
            Dictionary of mapping vectors
        TUStock : DataFrame
            Number of TU in the society [TU]
        TUTransportEnergyConsumption : DataFrame
            Vehicles energy consumption [J/km]
        TUTransportIntensityOfUse : DataFrame
            Vehicles intensity of use [km/year/vehicle]
        TUBuildingTUIndustryEnergyConsumption : DataFrame
            Buildings energy consumption [J/building unit]

        Output attributes
        ----------------
        EnergyDemandFinalTUDemand : DataFrame
            Total energy demand for the transport, building and industrial sectors [J/year]

        Notes
        -----
        Stock start :
            Transport sector :
        .. math:: \text{Energy demand [J/year]} = \text{Stock [TU]}\times\text{Consumption [J/km]}\times\text{Intensity of use [km/TU/year]}
        """

        self.EnergyDemandFinalTUDemand[i].loc[["LogisticalStart"], :, :, self.vector["TUTransport"], :] = (
            self.TUStock[i]
            .loc[["LogisticalStart"], :, :, self.vector["TUTransport"], :]
            .mul(
                concat_(
                    ["LogisticalStart"],
                    "Approach",
                    self.vector["CalculAll"],
                    "Calcul",
                    self.TUTransportEnergyConsumption[i].mul(self.TUTransportIntensityOfUse[i]),
                ),
                axis=0,
            )
        )

        self.EnergyDemandFinalTUDemand[i].loc[["LogisticalStart"], :, :, self.vector["TUBuilding"], :] = (
            self.TUStock[i]
            .loc[["LogisticalStart"], :, :, self.vector["TUBuilding"], :]
            .mul(
                concat_(
                    ["LogisticalStart"],
                    "Approach",
                    self.vector["CalculAll"],
                    "Calcul",
                    self.TUBuildingTUIndustryEnergyConsumption[i],
                ),
                axis=0,
            )
        )

    '''def impact_computation(self, i):
        """Computes the direct impacts of the society activities.

        The impacts of energy consumption and RM production.
        """
        self.ImpactEnergy[i] = (
            self.EnergyDemandPrimaryTotalEnergeticVector[i]
            .mul(self.ImpactEnergyConsumption[i])
            .groupby(level=["Approach", "Calcul", "Region", "Impact"])
            .sum()
        )
        self.ImpactResources[i] = (
            self.ResourcesFlowPrimary[i]
            .mul(self.ImpactResourcesProduction[i])
            .groupby(level=["Approach", "Calcul", "Region", "Impact"])
            .sum()
        )
        self.ImpactTotal[i] = self.ImpactEnergy[i] + self.ImpactResources[i]'''

    def mater_pre_processing(
        self,
        simulation_start_time=1901,
        simulation_end_time=2100,
        sampling_period=1,
        approach=None,
        calcul=None,
        region=None,
        smouth_time=10,
        iterations=3,
    ):
        """Runs the pre processing methods of MATER."""
        self.simulation_start_time = simulation_start_time
        self.simulation_end_time = simulation_end_time
        self.sampling_period = sampling_period  # Year
        self.smooth_tu_energy_production = smouth_time  # Year
        self.j_to_toe = 1.1868e10
        self.conversion = 1e-06 / (self.sampling_period * 365 * 24 * 3600)  # MW/J
        self.share_energy_industry_other = 0.55
        self.approach = approach
        self.calcul = calcul
        self.region = region
        self.iterations_number = iterations

        # Vectors definition

        start = t.time()
        print("\nVectors definition...")

        self.mapper_setting()
        self.mapping_vector_definition()

        end = t.time()
        print(end - start, "s")

        # Exogenous inputs definition

        start = t.time()
        print("\nExogenous variables definition...")

        self.socio_economic_inputs_definition()
        self.energy_demand_inputs_definition()
        self.TU_stock_inputs_definition()
        self.energy_consumption_inputs_definition()
        self.embodied_energy_inputs_definition()
        self.energy_production_inputs_definition()
        self.impact_inputs_definition()
        self.lifetime_inputs_definition()
        self.RM_inputs_definition()
        self.resources_inputs_definition()
        self.trade_inputs_definition()
        self.years_dataframe_definition()

        end = t.time()
        print(end - start, "s")

        # Endogenous variables definition

        start = t.time()
        print("\nEndogenous variables definition...")

        self.TU_variables_definition()
        self.TURM_variables_definition()
        self.TUYear_variables_definition()
        self.TU_EnergeticVector_variables_definition()
        self.RM_variables_definition()
        self.EnergeticVector_variables_definition()
        self.Resources_variables_definition()
        self.impact_variables_definition()
        self.differential_variable_definition()

        end = t.time()
        print(end - start, "s")

        # Energy start and stock start TUStock and EnergyDemand computation

        start = t.time()
        print("\nTUStock and EnergyDemand computation...")

        self.ResourcesProductionProcessTotal_computation()
        self.stock_computation()
        self.energy_demand_computation()
        self.TUStockInUse_initialization()

        end = t.time()
        print(end - start, "s")

    def mater_time_loop(self, i):
        """Runs one time iteration of MATER for GEMMES."""

        self.stock_computation_logistical_start_battery_tire(i)
        self.energy_demand_computation_logistical_start(i)
        self.current_stock_update(i)
        self.end_of_life_flow_computation(i)

        for _ in np.arange(1, self.iterations_number + 1, 1):

            self.parc_renewal(i)
            self.recycling_loop(i)
            self.Resources_flow_computation(i)
            self.industry_freight_stock_computation(i)
            self.energy_final_consumption_computation(i)
            self.electricity_production_computation(i)
            self.energy_primary_demand_computation(i)
            self.stock_electricity_production_computation(i)

        self.impact_computation(i)

    def gemmes_mater_test(self):
        """Tests the time loop iterations."""

        self.mater_pre_processing(
            simulation_end_time=1910,
            approach=["LogisticalStart"],
            calcul=["Endogenous"],
            region=["World"],
        )

        start = t.time()
        print("\nTime loop computation...")

        for i in np.arange(
            self.simulation_start_time,
            self.simulation_end_time + 1,
            self.sampling_period,
        ):

            print(i)
            self.mater_time_loop(i)

        end = t.time()
        print(end - start, "s")

    def GEMMES_to_MATER(self, GDP, year):
        """
        This method takes the GDP and modify the value of the GDP per capita in the Dataframe.

        INPUTS:
            GDP : float : GDP provided by GEMMES
            year : int : current year
        """

        self.GDPperCapita.loc["World", year] = (GDP*1.E12)/self.Population.loc["World", year]
        print('WARNING: GDP IN MATER IS APPROX TWHO TIMES GDP IN GEMMES')

    def MATER_to_GEMMES(self, year):
        """
        This method takes the total emissions and total population from MATER to GEMMES.

        INPUTS:
            year : int : current year

        OUTPUTS:
            Eco2eq : float : Total Emissions
            Npop : float : Total population
        """

        # tmp = self.Population.loc["World", 2015]/1.E9 # in billion
        # print(4.83/tmp)

        Npopm = self.Population.loc["World", year] / 1.E9  # in billion
        Npopp = self.Population.loc["World", year + 1] / 1.E9  # in billion
        Npop = np.linspace(start=Npopm, stop=Npopp, num=13)[:12]

        # Conversion factor for CO2-eq
        # from https://fr.wikipedia.org/wiki/Potentiel_de_r%C3%A9chauffement_global
        ch4_to_co2 = 28.
        n2o_to_co2 = 265.

        Eco2m = self.ImpactTotal.loc["LogisticalStart", "Endogenous", "World", "Carbon dioxide"][year - 1]
        Ech4m = self.ImpactTotal.loc["LogisticalStart", "Endogenous", "World", "Methane"][year - 1]
        En2om = self.ImpactTotal.loc["LogisticalStart", "Endogenous", "World", "Dinitrogen monoxide"][year - 1]

        Eco2p = self.ImpactTotal.loc["LogisticalStart", "Endogenous", "World", "Carbon dioxide"][year]
        Ech4p = self.ImpactTotal.loc["LogisticalStart", "Endogenous", "World", "Methane"][year]
        En2op = self.ImpactTotal.loc["LogisticalStart", "Endogenous", "World", "Dinitrogen monoxide"][year]

        Eco2eqm = (Eco2m + Ech4m * ch4_to_co2 + En2om * n2o_to_co2) / 1.E9
        Eco2eqp = (Eco2p + Ech4p * ch4_to_co2 + En2op * n2o_to_co2) / 1.E9

        Eco2eq = np.linspace(start=Eco2eqm, stop=Eco2eqp, num=13)[:12]

        return Eco2eq, Npop


if __name__ == "__main__":

    scenario = GemmesMater()

    scenario.load("data/data/MATER Monde3 data2.mater")

    scenario.gemmes_mater_test()
