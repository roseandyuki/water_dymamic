    def annu_water_budget(self, dby_flux):
        # Huangxiao for DNDC100: 删除的逻辑已省略

        # 修改后的逻辑
        self.day_transp = self.DayPT2

        # 当天蒸发量（雪 + 叶 + 积水 + 土壤）
        self.day_evapor = self.day_snow_ev + self.dfol_ev + self.day_pond_ev + self.day_soil_ev
        
        # 当天蒸散量（雪 + 叶 + 积水 + 蒸腾 + 土壤）
        self.day_ET = (
            self.day_snow_ev
            + self.dfol_ev
            + self.day_pond_ev
            + self.day_transp
            + self.day_soil_ev
        )

        # 年降水累计
        self.yr_prec_water += self.precipitation

        # 年旁路水流
        self.yr_bypass_in += self.day_bypass_influx
        self.day_bypass_influx = 0.0

        # 年蒸发细分累计
        self.yr_snow_ev += self.day_snow_ev
        self.yr_fol_ev += self.dfol_ev
        self.yr_pond_ev += self.day_pond_ev

        # 年总蒸散和截留
        self.yr_ET += self.day_ET
        self.yr_intercept += self.day_intercept