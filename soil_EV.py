    def soil_EV(self, hr, hrsoil_ev, DayFlux, hrPE3):
        EVL = int(0.2 / self.h[1])
        hrsoil_ev = 0.0

        # 计算覆盖系数 fsl
        self.surface_litter = self.rcvl[1] + self.rcl[1] + self.rcr[1] + self.stub1 + self.stub2 + self.stub3
        residue_volume = self.surface_litter / 100.0 / 10000.0  # m³/m²

        if self.surface_litter > 0.0:
            fsl = -0.99 - 0.236 * math.log(residue_volume)
            if fsl > 1.0:
                fsl = 1.0
        else:
            fsl = 1.0

        for l in range(1, EVL + 1):
            sev = hrPE3 * pow(0.5, l)  # 蒸发深度递减

            # 覆盖系数 limit1
            if self.FilmCoverFraction > 0.0:
                limit1 = 1.0 - self.FilmCoverFraction
            elif self.irri_flag == 1 and self.IrriMethod == 0:
                limit1 = 2.0
            else:
                limit1 = 1.0

            wiltptw = self.h[l] * self.sts[l] * self.wiltpt[l]
            fldcapw = self.h[l] * self.sts[l] * self.fldcap[l]

            # 土壤湿度限制系数 limit2
            if self.water[hr][l] < fldcapw:
                limit2 = (self.water[hr][l] - 0.0) / (fldcapw - 0.0)
                if limit2 < 0.0:
                    limit2 = 0.0
                limit2 = pow(limit2, self.qstar)
            else:
                limit2 = 1.0

            # 最终蒸发限制系数
            limit = limit1 * limit2 * fsl
            limit = max(0.0, min(1.0, limit))

            # 如果是水田且地表有积水，蒸发限制大幅降低
            if self.st[1] >= 12 and self.day_WT > 0.0:
                limit *= 0.01

            asev = sev * limit
            if asev < 0.0:
                asev = 0.0

            # 有地表径流旁路流时，额外损失水分
            if self.by_passf > 0.0:
                asev += (0.0001 * self.water[hr][l])

            if asev <= 0.0005 * wiltptw:
                asev = 0.0

            self.day_layer_soil_ev[l] += asev

            if self.water[hr][l] > asev:
                self.water[hr][l] -= asev
            else:
                asev = self.water[hr][l]
                self.water[hr][l] = 0.0

            hrsoil_ev += asev

            if self.st[1] >= 12 and self.day_WT > 0.0:
                self.water[hr][l] = fldcapw

        return hrsoil_ev