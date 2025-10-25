    def wetland_water_delivery(self, hr, hrsoil_ev, DayFlux, hrPE3):
        if self.total_ice == 0.0:
            for l in range(1, self.q + 1):
                ps = self.h[l] * self.sts[l]

                # bypass flow
                if self.byflow > 0.0 and l < self.WTL:
                    W01 = (self.fldcap[l] - self.water[hr][l] / ps) / (self.fldcap[l] - self.wiltpt[l])
                    if W01 >= 1.0:
                        DeliWater = self.byflow
                    elif W01 <= 0.0:
                        DeliWater = 0.0
                    else:
                        DeliWater = 0.01 * self.byflow * W01

                    if DeliWater > self.byflow:
                        DeliWater = self.byflow

                    self.water[hr][l] += DeliWater
                    self.byflow -= DeliWater
                    if self.byflow < 0.0:
                        self.byflow = 0.0

                    self.day_bypass_influx += DeliWater
                    DeliWater = 0.0
                else:
                    DeliWater = 0.0

                if l < self.WTL:
                    if l == 1:
                        AvaWater = self.surf_water
                        self.surf_water = 0.0
                        self.day_water_in += AvaWater
                    else:
                        AvaWater = self.OutWater[l - 1][hr]

                    self.water[hr][l] += AvaWater
                    AvaWater = 0.0

                    if self.water[hr][l] > ps:
                        sw = self.water[hr][l] - ps
                        self.water[hr][l] = ps
                        self.surf_water += sw
                        if l == 1:
                            self.day_water_in -= sw
                        sw = 0.0

                    travelt = 20.0 * (self.h[l] * self.sts[l] - self.h[l] * self.sts[l] * self.fldcap[l]) / self.sks[l]
                    TravelT = 0.5 * pow(self.clay[l], 1.9188) * travelt

                    wiltptw = self.h[l] * self.sts[l] * self.wiltpt[l]
                    fldcapw = self.h[l] * self.sts[l] * self.fldcap[l]

                    if self.water[hr][l] > fldcapw:
                        self.OutWater[l][hr] = 0.1 * (self.water[hr][l] - fldcapw) * (1.0 - 0.9 * pow(math.e, -1.0 / TravelT))
                        self.water[hr][l] -= self.OutWater[l][hr]
                    else:
                        self.OutWater[l][hr] = 0.0
                else:
                    # l >= WTL
                    self.water[hr][l] = ps

        # Wetland leaching
        self.day_leach_water += self.WaterLeakRate / 24.0
        return hrsoil_ev