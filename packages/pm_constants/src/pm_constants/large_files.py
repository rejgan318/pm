"""
ссылки на файлы для тестирования скорости при скачивании
"""
from enum import Enum

class LargeFiles(Enum):
    fr512K = "http://test-debit.free.fr/512.rnd"
    fr1MB = "http://test-debit.free.fr/1024.rnd"
    fr2MB = "http://test-debit.free.fr/2048.rnd"
    fr4MB = "http://test-debit.free.fr/4096.rnd"
    fr8MB = "http://test-debit.free.fr/8192.rnd"
    fr16MB = "http://test-debit.free.fr/16384.rnd"
    fr32MB = "http://test-debit.free.fr/32768.rnd"
    fr64MB = "http://test-debit.free.fr/65536.rnd"
    fr1GB = "http://test-debit.free.fr/1048576.rnd"
    fr10GB = "http://test-debit.free.fr/10485760.rnd"

    ov1MB = "https://proof.ovh.net/files/1Mb.dat"
    ov10MB = "https://proof.ovh.net/files/10Mb.dat"
    ov100MB = "https://proof.ovh.net/files/100Mb.dat"
    ov1GB = "https://proof.ovh.net/files/1Gb.dat"
    ov10GB = "https://proof.ovh.net/files/10Gb.dat"
