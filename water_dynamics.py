    def water_dynamics(self):
        # 调用逐小时水分循环
        self.dby_flux, self.DayFlux = self.hour_loop(self.DayFlux, self.dby_flux)

        # 原 C++ 注释掉了 daily_WT()
        # 如果需要启用可取消注释
        # self.daily_WT()

        # 将日水通量置零
        self.zero_DayFlux()

        # 年度水量平衡计算
        self.annu_water_budget(self.dby_flux)