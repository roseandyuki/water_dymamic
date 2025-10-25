    def pond_water_bypass_flux(self, Throufall):
        if self.st[1] < 12:
            if self.SCSuse == 0:
                if Throufall > 0.0 and self.sslope > 0.0:
                    aslope = self.sslope / 90.0  # degree -> fraction
                    if self.total_ice > 0.0:
                        aslope = 0.9
                    if aslope > 1.0:
                        aslope = 1.0

                    self.runoff_pool += aslope * Throufall  # m water/day
                    Throufall *= (1.0 - aslope)
            else:
                if self.scs_runoff > 0.0:
                    if self.scs_runoff >= Throufall:
                        hr_runoff = Throufall
                        self.scs_runoff -= hr_runoff
                        Throufall = 0.0
                    else:
                        hr_runoff = self.scs_runoff
                        self.scs_runoff = 0.0
                        Throufall -= hr_runoff

                    self.runoff_pool += hr_runoff  # m water/day

        # modified by Huangxiao for DNDC100
        if self.snow_pack > 0:
            self.runoff_pool += Throufall
        else:
            self.surf_water += Throufall

        Throufall = 0.0

        if (self.surf_water > 0.0 and
            self.by_passf > 0.0 and
            self.total_ice == 0.0 and
            self.WRL > self.q):
            self.byflow = self.surf_water * self.by_passf
            self.surf_water -= self.byflow
        else:
            self.byflow = 0.0