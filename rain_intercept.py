    def rain_intercept(self, hr):
        Tlai = self.lai[1] + self.lai[2] + self.lai[3]
        max_leaf_water = Tlai * 0.0001  # m water

        self.f_TTT = 1.0

        if self.precipitation > 0.0 and self.air_temp > 0.0:
            Intercept = 0.0
            if self.TTT > 24.0:
                Throufall = self.precipitation / 24.0
            else:
                if hr <= int(self.TTT):
                    Throufall = 0.005
                elif hr == int(self.TTT) + 1:
                    Throufall = 0.005 * (self.TTT - int(self.TTT))
                else:
                    Throufall = 0.0
        else:
            Intercept = 0.0
            Throufall = 0.0
        
        return Throufall, Intercept