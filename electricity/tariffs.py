"""
Map a given datetime to a tariff
"""
__version__ = "0.0.1"
__author__ = "Diogo Gomes"
__email__ = "diogogomes@gmail.com"

from datetime import date, time, datetime, timedelta
from dateutil.parser import parse

MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY = range(7)
WEEKEND = (SATURDAY, SUNDAY)

PT = "Portugal"


class EnergyOperator:
    def __init__(self, country, operator_name):
        self.operator_name = operator_name
        self.country = country

    @classmethod
    def tariffs(self):
        """Return list of tariffs."""
        pass

    @classmethod
    def tariff_periods(self):
        """Return list of tariff periods."""
        pass

    def __str__(self):
        return self.operator_name


class ERSE(EnergyOperator):
    NORMAL = "Normal"
    PONTA = "Ponta"
    CHEIAS = "Cheias"
    VAZIO_NORMAL = "Vazio Normal"
    SUPER_VAZIO = "Super Vazio"
    _tariffs = [PONTA, CHEIAS, VAZIO_NORMAL, SUPER_VAZIO]

    def __init__(self):
        super().__init__(PT, "Entidade Reguladora dos Serviços Energéticos")

    @classmethod
    def tariffs(self):
        return self._tariffs

    @classmethod
    def tariff_periods(self):
        return self._tariff_periods.keys()

    @classmethod
    def in_time_range(cls, hour_start, minute_start, t, hour_stop, minute_stop):
        print(hour_start, minute_start, t, hour_stop, minute_stop)
        return time(hour_start, minute_start) <= t.time() < time(hour_stop, minute_stop)

    @classmethod
    def is_summer(cls, time):
        # Hora legal de Verão começa no 1º Domingo de Março e acaba no ultimo de Outubro
        # https://docs.python.org/3.3/library/datetime.html
        d = datetime(time.year, 4, 1)
        i_verao = d - timedelta(days=d.weekday() + 1)
        d = datetime(time.year, 11, 1)
        f_verao = d - timedelta(days=d.weekday() + 1)
        if i_verao <= time.replace(tzinfo=None) < f_verao:
            return True
        return False

    @classmethod
    def ciclo_semanal_continente(self, time):
        # From http://www.erse.pt/pt/electricidade/tarifaseprecos/periodoshorarios/Paginas/CicloSemanalTodosFornecPtCont.aspx
        if self.is_summer(time):
            # Verão
            if 0 <= time.weekday() < 5:
                # Seg a Sex
                if self.in_time_range(9, 15, time, 12, 15):
                    return self.PONTA
                if self.in_time_range(7, 0, time, 9, 15) or self.in_time_range(
                    12, 15, time, 24, 0
                ):
                    return self.CHEIAS
                if self.in_time_range(0, 0, time, 2, 0) or self.in_time_range(
                    6, 0, time, 7, 0
                ):
                    return self.VAZIO_NORMAL
                if self.in_time_range(2, 0, time, 6, 0):
                    return self.SUPER_VAZIO
            if time.weekday() == 5:
                # Sabado
                if self.in_time_range(9, 0, time, 14, 0) or self.in_time_range(
                    20, 0, time, 22, 0
                ):
                    return self.CHEIAS
                if (
                    self.in_time_range(0, 0, time, 2, 0)
                    or self.in_time_range(6, 0, time, 9, 0)
                    or self.in_time_range(14, 0, time, 20, 0)
                    or self.in_time_range(22, 0, time, 24, 0)
                ):
                    return self.VAZIO_NORMAL
                if self.in_time_range(2, 0, time, 6, 0):
                    return self.SUPER_VAZIO
            if time.weekday() == 6:
                # Domingo
                if self.in_time_range(0, 0, time, 2, 0) or self.in_time_range(
                    6, 0, time, 24, 0
                ):
                    return self.VAZIO_NORMAL
                if self.in_time_range(2, 0, time, 6, 0):
                    return self.SUPER_VAZIO
        else:
            # Inverno
            if 0 <= time.weekday() < 5:
                # Seg a Sex
                if self.in_time_range(9, 30, time, 12, 00) or self.in_time_range(
                    18, 30, time, 21, 0
                ):
                    return self.PONTA
                if (
                    self.in_time_range(7, 0, time, 9, 30)
                    or self.in_time_range(12, 0, time, 18, 30)
                    or self.in_time_range(21, 0, time, 24, 0)
                ):
                    return self.CHEIAS
                if self.in_time_range(0, 0, time, 2, 0) or self.in_time_range(
                    6, 0, time, 7, 0
                ):
                    return self.VAZIO_NORMAL
                if self.in_time_range(2, 0, time, 6, 0):
                    return self.SUPER_VAZIO
            if time.weekday() == 5:
                # Sabado
                if self.in_time_range(9, 30, time, 13, 0) or self.in_time_range(
                    18, 30, time, 22, 0
                ):
                    return self.CHEIAS
                if (
                    self.in_time_range(0, 0, time, 2, 0)
                    or self.in_time_range(6, 0, time, 9, 30)
                    or self.in_time_range(13, 0, time, 18, 30)
                    or self.in_time_range(22, 0, time, 24, 0)
                ):
                    return self.VAZIO_NORMAL
                if self.in_time_range(2, 0, time, 6, 0):
                    return self.SUPER_VAZIO
            if time.weekday() == 6:
                # Domingo
                if self.in_time_range(0, 0, time, 2, 0) or self.in_time_range(
                    6, 0, time, 24, 0
                ):
                    return self.VAZIO_NORMAL
                if self.in_time_range(2, 0, time, 6, 0):
                    return self.SUPER_VAZIO

    @classmethod
    def ciclo_diario_continente(self, time):
        # From http://www.erse.pt/pt/electricidade/tarifaseprecos/periodoshorarios/Paginas/CiclodiariofornecBTEBTNPt.aspx
        if self.is_summer(time):
            # Verão
            if self.in_time_range(10, 30, time, 13, 00) or self.in_time_range(
                19, 30, time, 21, 0
            ):
                return self.PONTA
            if (
                self.in_time_range(8, 0, time, 10, 30)
                or self.in_time_range(13, 0, time, 19, 30)
                or self.in_time_range(21, 0, time, 22, 0)
            ):
                return self.CHEIAS
            if (
                self.in_time_range(6, 0, time, 8, 0)
                or self.in_time_range(22, 0, time, 24, 0)
                or self.in_time_range(0, 0, time, 2, 0)
            ):
                return self.VAZIO_NORMAL
            if self.in_time_range(2, 0, time, 6, 0):
                return self.SUPER_VAZIO
        else:
            # Inverno
            if self.in_time_range(9, 0, time, 10, 30) or self.in_time_range(
                18, 0, time, 20, 30
            ):
                return self.PONTA
            if (
                self.in_time_range(8, 0, time, 9, 0)
                or self.in_time_range(10, 30, time, 18, 0)
                or self.in_time_range(20, 30, time, 22, 0)
            ):
                return self.CHEIAS
            if (
                self.in_time_range(6, 0, time, 8, 0)
                or self.in_time_range(22, 0, time, 24, 0)
                or self.in_time_range(0, 0, time, 2, 0)
            ):
                return self.VAZIO_NORMAL
            if self.in_time_range(2, 0, time, 6, 0):
                return self.SUPER_VAZIO


class EDP(ERSE):
    VAZIO = "Vazio"
    FORA_VAZIO = "Fora de Vazio"
    _tariffs = [ERSE.PONTA, ERSE.CHEIAS, VAZIO, FORA_VAZIO]

    def simples(self):
        return self.NORMAL

    def bi_horario_diario(self, time):
        if ERSE.ciclo_diario_continente(time) in [ERSE.VAZIO_NORMAL, ERSE.SUPER_VAZIO]:
            return self.VAZIO
        return self.FORA_VAZIO

    def bi_horario_semanal(self, time):
        if ERSE.ciclo_semanal_continente(time) in [ERSE.VAZIO_NORMAL, ERSE.SUPER_VAZIO]:
            return self.VAZIO
        return self.FORA_VAZIO

    def tri_horario_diario(self, time):
        current = ERSE.ciclo_diario_continente(time)
        if current in [ERSE.VAZIO_NORMAL, ERSE.SUPER_VAZIO]:
            return self.VAZIO
        else:
            return current

    def tri_horario_semanal(self, time):
        current = ERSE.ciclo_semanal_continente(time)
        if current in [ERSE.VAZIO_NORMAL, ERSE.SUPER_VAZIO]:
            return self.VAZIO
        else:
            return current

    _tariff_periods = {
        "Simples": simples,
        "Bi-horário - ciclo diário": bi_horario_diario,
        "Bi-horário - ciclo semanal": bi_horario_semanal,
        "Tri-horário - ciclo diário": tri_horario_diario,
        "Tri-horário - ciclo semanal": tri_horario_semanal,
    }


class Galp(ERSE):
    VAZIO = "Vazio"
    FORA_VAZIO = "Fora de Vazio"
    _tariffs = [VAZIO, FORA_VAZIO]

    def simples(self):
        return self.NORMAL

    def bi_horario_diario(self, time):
        if ERSE.ciclo_diario_continente(time) in [ERSE.VAZIO_NORMAL, ERSE.SUPER_VAZIO]:
            return self.VAZIO
        return self.FORA_VAZIO

    def bi_horario_semanal(self, time):
        if ERSE.ciclo_semanal_continente(time) in [ERSE.VAZIO_NORMAL, ERSE.SUPER_VAZIO]:
            return self.VAZIO
        return self.FORA_VAZIO

    _tariff_periods = {
        "Simples": simples,
        "Bi-horário - ciclo diário": bi_horario_diario,
        "Bi-horário - ciclo semanal": bi_horario_semanal,
    }


COUNTRIES = {PT: {"EDP": EDP, "Galp": Galp}}