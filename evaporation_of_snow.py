    def evaporation_of_snow(self, hrPE2):
        if self.snow_pack > 0.0 and hrPE2 > 0.0:
            if self.snow_pack >= hrPE2:
                hrsnow_ev = hrPE2
                self.snow_pack -= hrPE2
                hrPE3 = 0.0
            else:
                hrsnow_ev = self.snow_pack
                hrPE3 = hrPE2 - self.snow_pack
                self.snow_pack = 0.0
        else:
            hrPE3 = hrPE2
            hrsnow_ev = 0.0

        return hrsnow_ev, hrPE3