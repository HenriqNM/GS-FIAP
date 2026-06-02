logs_telemetria = [
    {"sensor": "bateria_m1", "leitura": 13.2, "unidade": "V", "timestamp": "2026-05-26T10:00:00"},
    {"sensor": "temp_nucleo", "leitura": 72.0, "unidade": "C", "timestamp": "2026-05-26T10:00:15"},
    {"sensor": "pressao_cabine", "leitura": 12.5, "unidade": "psi", "timestamp": "2026-05-26T10:00:30"},
    {"sensor": "sensor_proximidade", "leitura": 380.5, "unidade": "cm", "timestamp": "2026-05-26T10:00:45"},

    {"sensor": "bateria_m1", "leitura": 12.8, "unidade": "V", "timestamp": "2026-05-26T10:01:00"},
    {"sensor": "temp_nucleo", "leitura": 75.5, "unidade": "C", "timestamp": "2026-05-26T10:01:15"},
    {"sensor": "pressao_cabine", "leitura": 12.8, "unidade": "psi", "timestamp": "2026-05-26T10:01:30"},
    {"sensor": "sensor_proximidade", "leitura": 290.0, "unidade": "cm", "timestamp": "2026-05-26T10:01:45"},

    {"sensor": "bateria_m1", "leitura": 12.2, "unidade": "V", "timestamp": "2026-05-26T10:02:00"},
    {"sensor": "temp_nucleo", "leitura": 80.1, "unidade": "C", "timestamp": "2026-05-26T10:02:15"},
    {"sensor": "pressao_cabine", "leitura": 13.1, "unidade": "psi", "timestamp": "2026-05-26T10:02:30"},
    {"sensor": "sensor_proximidade", "leitura": 148.2, "unidade": "cm", "timestamp": "2026-05-26T10:02:45"},

    {"sensor": "bateria_m1", "leitura": 10.5, "unidade": "V", "timestamp": "2026-05-26T10:03:00"},
    {"sensor": "temp_nucleo", "leitura": 85.3, "unidade": "C", "timestamp": "2026-05-26T10:03:15"},
    {"sensor": "pressao_cabine", "leitura": 14.8, "unidade": "psi", "timestamp": "2026-05-26T10:03:30"},
    {"sensor": "sensor_proximidade", "leitura": 85.3, "unidade": "cm", "timestamp": "2026-05-26T10:03:45"},

    {"sensor": "bateria_m1", "leitura": 10.1, "unidade": "V", "timestamp": "2026-05-26T10:04:00"},
    {"sensor": "temp_nucleo", "leitura": 89.5, "unidade": "C", "timestamp": "2026-05-26T10:04:15"},
    {"sensor": "pressao_cabine", "leitura": 11.9, "unidade": "psi", "timestamp": "2026-05-26T10:04:30"},
    {"sensor": "sensor_proximidade", "leitura": 32.7, "unidade": "cm", "timestamp": "2026-05-26T10:04:45"},

    # DADOS CORROMPIDOS PARA TESTE DE EXCEÇÃO

    {"sensor": "bateria_m1", "leitura": "DISCONNECTED", "unidade": "V", "timestamp": "2026-05-26T10:05:00"},
    {"sensor": "temp_nucleo", "unidade": "C", "timestamp": "2026-05-26T10:05:15"},
    {"sensor": "sensor_fantasma_99", "leitura": 45.2, "unidade": "N/A", "timestamp": "2026-05-26T10:05:30"},
    {"sensor": "pressao_cabine", "leitura": [12.5, 13.0], "unidade": "psi", "timestamp": "2026-05-26T10:05:45"},
    ["sensor_proximidade", 0.0, "cm"]
]