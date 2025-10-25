    def paddy_water_delivery(self, hr, hrsoil_ev, DayFlux, hrPE3):
        leak_water = self.WaterLeakRate / 24.0

        for l in range(1, self.q + 1):
            # 漏水与地表水的关系
            if leak_water / self.q <= self.surf_water:
                self.day_leach_water += leak_water / self.q
                self.surf_water -= leak_water / self.q
            else:
                fldcapw = self.h[l] * self.sts[l] * self.fldcap[l]
                if self.water[hr][l] <= fldcapw:
                    self.day_leach_water += self.surf_water
                    self.surf_water = 0.0
                else:
                    if self.surf_water + self.water[hr][l] - fldcapw > leak_water / self.q:
                        self.day_leach_water += leak_water / self.q
                        self.water[hr][l] -= leak_water / self.q - self.surf_water
                        self.surf_water = 0.0
                    else:
                        self.day_leach_water += self.surf_water + self.water[hr][l] - fldcapw
                        self.water[hr][l] = fldcapw
                        self.surf_water = 0.0

            # 补齐土壤孔隙水
            ps = self.h[l] * self.sts[l]
            if self.water[hr][l] < ps:
                gap = ps - self.water[hr][l]
                if gap <= self.surf_water:
                    self.water[hr][l] = ps
                    self.surf_water -= gap
                else:
                    self.water[hr][l] += self.surf_water
                    self.surf_water = 0.0

        return hrsoil_ev