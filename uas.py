from multiprocessing.sharedctypes import Value


def down(x, xmin, xmax):
    return (xmax- x) / (xmax - xmin)

def up(x, xmin, xmax):
    return (x - xmin) / (xmax - xmin)

class Permintaan():
    minimum = 2100
    maximum = 3500

    def turun(self, x):
        if x >= self.maximum:
            return 0
        elif x <= self.minimum:
            return 1
        else:
            return down(x, self.minimum, self.maximum)

    def naik(self, x):
        if x >= self.maximum:
            return 1
        elif x <= self.minimum:
            return 0
        else:
            return up(x, self.minimum, self.maximum)

class Persediaan():
    value1 = 118
    value2 = 237
    value3 = 343
    value4 = 564
    value5 = 780

    def sedikit(self, x):
        if x >= self.value2:
            return 0
        elif x <= self.value1:
            return 1
        else:
            return down(x, self.value1, self.value2)
    
    def cukup(self, x):
        if self.value1 < x < self.value2:
            return up(x, self.value1, self.value2)
        elif self.value2 < x < self.value3:
            return down(x, self.value2, self.value3)
        elif x == self.value2:
            return 1
        else:
            return 0

    def banyak(self, x):
        if self.value2 < x < self.value3:
            return up(x, self.value2, self.value3)
        elif self.value3 < x < self.value4:
            return down(x, self.value3, self.value4)
        elif x == self.value3:
            return 1
        else:
            return 0

    def cukup_banyak(self, x):
        if self.value3 < x < self.value4:
            return up(x, self.value3, self.value4)
        elif self.value4 < x < self.value5:
            return down(x, self.value4, self.value5)
        elif x == self.value4:
            return 1
        else:
            return 0

    def sangat_banyak(self, x):
        if x >= self.value5:
            return 1
        elif x <= self.value4:
            return 0
        else:
            return up(x, self.value4, self.value5)

class Produksi():
    minimum = 1000
    maximum = 5000
    
    def kurang(self, x):
        return self.maximum - x * (self.maximum-self.minimum)

    def tambah(self, x):
        return x * (self.maximum - self.minimum) + self.minimum

    # 2 permintaan * 5 persediaan
    # rule === 10
    def inferensi(self, jumlah_permintaan, jumlah_persediaan):
        pmt = Permintaan()
        psd = Persediaan()
        result = []

        # [R1] pmt turun, psd sedikit => produksi.kurang
        a1 = min(pmt.turun(jumlah_permintaan), psd.sedikit(jumlah_persediaan))
        z1 = self.kurang(a1)
        result.append((a1, z1))

        # [R2] pmt naik, psd sedikit => produksi.tambah
        a2 = min(pmt.naik(jumlah_permintaan), psd.sedikit(jumlah_persediaan))
        z2 = self.tambah(a2)
        result.append((a2, z2))

        # [R3] pmt turun, psd cukup => produksi.kurang
        a3 = min(pmt.turun(jumlah_permintaan), psd.cukup(jumlah_persediaan))
        z3 = self.kurang(a3)
        result.append((a3, z3))

        # [R4] pmt naik, psd cukup => produksi.naik
        a4 = min(pmt.naik(jumlah_permintaan), psd.cukup(jumlah_persediaan))
        z4 = self.tambah(a4)
        result.append((a4, z4))

        # [R5] pmt turun, psd banyak => produksi.kurang
        a5 = min(pmt.turun(jumlah_permintaan), psd.banyak(jumlah_persediaan))
        z5 = self.kurang(a5)
        result.append((a5, z5))

        # [R6] pmt naik, psd banyak => produksi.naik
        a6 = min(pmt.naik(jumlah_permintaan), psd.banyak(jumlah_persediaan))
        z6 = self.tambah(a6)
        result.append((a6, z6))

        # [R7] pmt turun, psd cukup_banyak => produksi.kurang
        a7 = min(pmt.turun(jumlah_permintaan), psd.cukup_banyak(jumlah_persediaan))
        z7 = self.kurang(a7)
        result.append((a7, z7))

        # [R8] pmt naik, psd cukup_banyak => produksi.naik
        a8 = min(pmt.naik(jumlah_permintaan), psd.cukup_banyak(jumlah_persediaan))
        z8 = self.tambah(a8)
        result.append((a8, z8))

        # [R9] pmt turun, psd sangat_banyak => produksi.kurang
        a9 = min(pmt.turun(jumlah_permintaan), psd.sangat_banyak(jumlah_persediaan))
        z9 = self.kurang(a9)
        result.append((a9, z9))

        # [R10] pmt naik, psd sangat_banyak => produksi.tambah
        a10 = min(pmt.naik(jumlah_permintaan), psd.sangat_banyak(jumlah_persediaan))
        z10 = self.tambah(a10)
        result.append((a10, z10))

        return result
    
    def defuzifikasi(self, jumlah_permintaan, jumlah_persediaan):
        inferensi_values = self.inferensi(jumlah_permintaan, jumlah_persediaan)
        return sum([(value[0]* value[1]) for value in inferensi_values]) / sum([value[0] for value in inferensi_values])
