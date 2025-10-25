    def hour_loop(self, DayFlux, dby_flux):
        hrsoil_ev = 0.0
        # 年累计潜在蒸发
        self.yr_PE += self.act_DayPE
        self.hrPE0 = self.act_DayPE / 24.0

        self.dw = 0.0
        self.day_IrriWater = self.IrriWater

        for hr in range(1, 25):
            # 灌溉
            if self.IrriWater > 0.0:
                if self.IrriMethod == 0:  # furrow irrigation
                    dfIR = self.day_IrriWater / 5.0
                    self.surf_water += dfIR
                elif self.IrriMethod == 1:  # sprinkler
                    dfIR = self.day_IrriWater / 2.0
                    self.water[hr][5] += dfIR
                else:  # drip
                    dfIR = self.day_IrriWater / 20.0
                    DripD = int(0.05 / self.h[1])
                    self.water[hr][DripD] += dfIR

                self.IrriWater -= dfIR
                if self.IrriWater < 0.0:
                    self.IrriWater = 0.0

            # 叶面蒸发
            if self.leaf_water > 0.0:
                if self.hrPE0 * 0.5 < self.leaf_water:
                    self.leaf_water -= self.hrPE0 * 0.5
                    self.hrfol_ev = self.hrPE0 * 0.5
                    hrPE1 = self.hrPE0 * 0.5
                else:
                    self.hrfol_ev = self.leaf_water
                    hrPE1 = self.hrPE0 - self.leaf_water
                    self.leaf_water = 0.0
            else:
                self.hrfol_ev = 0.0
                hrPE1 = self.hrPE0

            self.dfol_ev += self.hrfol_ev

            # 雪蒸发
            hrPE2 = hrPE1
            hrsnow_ev, hrPE3 = self.evaporation_of_snow(hrPE2)
            self.day_snow_ev += hrsnow_ev

            # 水面蒸发
            if self.day_WT >= 0.0 and hr == 1:
                self.surf_water = self.day_WT

            if self.surf_water > 0.0:
                Ftt = 1.0
                Ftt = max(0.0, min(1.0, Ftt))

                if self.surf_water >= hrPE3:
                    hrPonding_ev = Ftt * hrPE3
                else:
                    hrPonding_ev = Ftt * self.surf_water
            else:
                hrPonding_ev = 0.0

            hrPE3 -= hrPonding_ev
            self.surf_water -= hrPonding_ev
            self.day_pond_ev += hrPonding_ev

            # 雨水截留
            Throufall, Intercept = self.rain_intercept(hr)
            self.day_intercept += Intercept

            # 表层水绕流
            self.pond_water_bypass_flux(Throufall)

            # 水分入渗与土壤蒸发
            if self.WaterControl == 1 or self.crop[1] == 30:
                hrsoil_ev = self.wetland_water_delivery(hr, hrsoil_ev, DayFlux, hrPE3)
                hrsoil_ev = self.soil_EV(hr, hrsoil_ev, DayFlux, hrPE3)
            else:
                if (self.IrriRice_flag == 1 or (self.wetland_flag == 1 and self.flood_flag == 1)) and self.IrriType == 1:
                    hrsoil_ev = self.paddy_water_delivery(hr, hrsoil_ev, DayFlux, hrPE3)
                    hrsoil_ev = self.soil_EV(hr, hrsoil_ev, DayFlux, hrPE3)
                else:
                    if self.total_ice == 0.0:
                        if self.paddysoil_flag:
                            hrsoil_ev = self.paddy_water_delivery(hr, hrsoil_ev, DayFlux, hrPE3)
                        else:
                            hrsoil_ev, DayFlux = self.water_delivery(hr, hrsoil_ev, DayFlux, hrPE3)
                        hrsoil_ev = self.soil_EV(hr, hrsoil_ev, DayFlux, hrPE3)

            # 小时水分向下传递
            if hr < 24:
                for l in range(1, self.q + 1):
                    self.water[hr + 1][l] = self.water[hr][l]

        # 日结束后汇总
        for l in range(1, self.q + 1):
            self.day_soil_ev += self.day_layer_soil_ev[l]
            self.day_layer_soil_ev[l] = 0.0

            ps = self.h[l] * self.sts[l]
            self.day_wfps[l] = self.water[24][l] / ps
            self.day_wfps[l] = min(1.0, max(1e-8, self.day_wfps[l]))

        # 地表水与径流调整
        if self.flood_flag == 0:
            WT_thold = WT_thold3 if self.paddysoil_flag else WT_thold4

            if self.snow_pack + self.surf_water + self.runoff_pool > WT_thold:
                if self.snow_pack > WT_thold:
                    self.day_runoff += self.runoff_pool
                    self.runoff_pool = 0.0
                elif self.snow_pack > 0.0:
                    excess = self.snow_pack + self.runoff_pool - WT_thold
                    self.day_runoff += excess
                    self.runoff_pool -= excess
                else:
                    self.day_runoff += self.surf_water - WT_thold
                    self.surf_water = WT_thold

        return dby_flux, DayFlux