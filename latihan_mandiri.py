import logging
from abc import ABC, abstractmethod

# Konfigurasi Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)

LOGGER = logging.getLogger("Registration")


# 1. Abstraksi
class IValidationRule(ABC):
    """
    Interface untuk semua aturan validasi registrasi mahasiswa.
    """

    @abstractmethod
    def validate(self, data: dict) -> bool:
        """
        Melakukan validasi berdasarkan aturan tertentu.

        Args:
            data (dict): Data mahasiswa yang akan divalidasi.

        Returns:
            bool: True jika valid, False jika tidak valid.
        """
        pass


# 2a. Aturan SKS
class SksLimitRule(IValidationRule):
    """
    Aturan validasi untuk membatasi total SKS mahasiswa.
    """

    def __init__(self, max_sks: int):
        """
        Inisialisasi batas maksimum SKS.

        Args:
            max_sks (int): Batas maksimum SKS.
        """
        self.max_sks = max_sks

    def validate(self, data: dict) -> bool:
        """
        Memvalidasi apakah total SKS tidak melebihi batas.

        Args:
            data (dict): Data mahasiswa.

        Returns:
            bool: True jika valid, False jika melebihi batas.
        """
        total_sks = data.get("total_sks", 0)

        if total_sks > self.max_sks:
            LOGGER.warning(
                f"Validasi Gagal: Total SKS {total_sks} melebihi batas {self.max_sks}."
            )
            return False

        LOGGER.info("Validasi SKS berhasil.")
        return True


# 2b. Aturan Prasyarat
class PrerequisiteRule(IValidationRule):
    """
    Aturan validasi untuk memastikan prasyarat mata kuliah terpenuhi.
    """

    def validate(self, data: dict) -> bool:
        """
        Memvalidasi apakah prasyarat mata kuliah telah terpenuhi.

        Args:
            data (dict): Data mahasiswa.

        Returns:
            bool: True jika terpenuhi, False jika belum.
        """
        prasyarat_ok = data.get("prasyarat_ok", False)

        if not prasyarat_ok:
            LOGGER.warning("Validasi Gagal: Prasyarat mata kuliah belum terpenuhi.")
            return False

        LOGGER.info("Validasi prasyarat berhasil.")
        return True


# 4. Aturan tambahan OCP (Challenge)
class JadwalBentrokRule(IValidationRule):
    """
    Aturan validasi untuk memastikan tidak ada jadwal bentrok.
    """

    def validate(self, data: dict) -> bool:
        """
        Memvalidasi apakah terdapat bentrok jadwal.

        Args:
            data (dict): Data mahasiswa.

        Returns:
            bool: True jika tidak bentrok, False jika bentrok.
        """
        bentrok = data.get("jadwal_bentrok", False)

        if bentrok:
            LOGGER.warning("Validasi Gagal: Terdapat jadwal bentrok.")
            return False

        LOGGER.info("Validasi jadwal berhasil.")
        return True


# 3. Service SRP + DIP
class RegistrationService:
    """
    Service untuk memproses validasi registrasi mahasiswa.
    """

    def __init__(self, rules: list[IValidationRule]):
        """
        Menginisialisasi service dengan daftar aturan validasi.

        Args:
            rules (list[IValidationRule]): Daftar rule validasi.
        """
        self.rules = rules

    def validate(self, data: dict) -> bool:
        """
        Menjalankan seluruh aturan validasi secara berurutan.

        Args:
            data (dict): Data mahasiswa.

        Returns:
            bool: True jika semua validasi lolos, False jika ada yang gagal.
        """
        LOGGER.info("=== MULAI VALIDASI REGISTRASI ===")

        for rule in self.rules:
            if not rule.validate(data):
                LOGGER.error(">>> VALIDASI REGISTRASI GAGAL")
                return False

        LOGGER.info(">>> VALIDASI REGISTRASI BERHASIL")
        return True


# 5. Program utama
if __name__ == "__main__":
    data_mhs = {
        "nama": "Andi",
        "total_sks": 22,
        "prasyarat_ok": True,
        "jadwal_bentrok": False
    }

    rules = [
        SksLimitRule(max_sks=24),
        PrerequisiteRule(),
        JadwalBentrokRule()
    ]

    service = RegistrationService(rules)
    service.validate(data_mhs)
