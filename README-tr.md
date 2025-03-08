# Shared Ledger System

Bu proje, bir monorepo içindeki birden fazla uygulama için paylaşılan bir ledger sistemi sağlar.

## Özellikler

- Tüm uygulamalar için ortak Ledger operasyonlarını zorunlu kılan tip güvenliği
- Merkezi implementasyon ile kod tekrarının önlenmesi
- Uygulama özelinde genişletilebilir operasyonlar
- FastAPI, SQLAlchemy 2.0, Pydantic ve PostgreSQL kullanımı

## Gereksinimler

- Python ≥ 3.10
- PostgreSQL
- Docker (opsiyonel)

## Kurulum

### Sanal Ortam Kurulumu

```bash
# Sanal ortam oluştur
python -m venv venv

# Sanal ortamı aktifleştir
# Windows için:
venv\Scripts\activate
# Unix/MacOS için:
source venv/bin/activate

# Bağımlılıkları yükle
pip install -e .
```

### Veritabanı Kurulumu

```bash
# PostgreSQL veritabanlarını oluştur
createdb -U postgres healthai
createdb -U postgres travelai

# Migrasyonları çalıştır
cd healthai
alembic upgrade head
cd ..

cd travelai
alembic upgrade head
cd ..
```

## Çalıştırma

```bash
# HealthAI uygulamasını çalıştır
cd healthai
uvicorn src.main:app --reload --port 8000

# TravelAI uygulamasını çalıştır (başka bir terminal penceresinde)
cd travelai
uvicorn src.main:app --reload --port 8001
```

Daha hızlı çalıştırmak için otomatik betik:

```bash
# Çalıştırma izni ver
chmod +x run.sh

# Çalıştır
./run.sh
```

## API Kullanımı

### Bakiye Sorgulama

```
GET /ledger/{owner_id}
```

#### Cevap:

```json
{
  "owner_id": "user123",
  "balance": 42,
  "last_updated": "2023-01-01T12:00:00Z"
}
```

### Yeni Ledger Kaydı Oluşturma

```
POST /ledger
```

#### İstek:

```json
{
  "owner_id": "user123",
  "operation": "CREDIT_ADD",
  "nonce": "unique-transaction-id-123"
}
```

#### Cevap:

```json
{
  "id": 1,
  "operation": "CREDIT_ADD",
  "amount": 10,
  "nonce": "unique-transaction-id-123",
  "owner_id": "user123",
  "created_on": "2023-01-01T12:00:00Z"
}
```

## Proje Yapısı

```
├── monorepo/
│   ├── core/
│   │   ├── db/
│   │   │   ├── models.py               # Temel SQLAlchemy modelleri
│   │   │   └── ledger_repository.py    # DB operasyonları için repository
│   │   ├── ledgers/
│   │   │   ├── services/
│   │   │   │   └── base_ledger_service.py  # Temel ledger servisi
│   │   │   ├── schemas.py              # Temel Enum tanımları
│   │   │   ├── pydantic_schemas.py     # Temel Pydantic modelleri
│   │   │   └── config.py               # Operasyon değerleri konfigürasyonu
│   ├── __init__.py
├── healthai/
│   ├── src/
│   │   ├── api/
│   │   │   ├── ledgers/
│   │   │   │   ├── models.py          # Uygulama-spesifik SQLAlchemy modeli
│   │   │   │   ├── router.py          # API endpoint'leri
│   │   │   │   └── schemas.py         # Uygulama-spesifik Enum'lar
│   │   │   ├── config.py             # Uygulama konfigürasyonu
│   │   │   └── db.py                 # DB bağlantısı
│   │   ├── main.py                  # Uygulama giriş noktası
│   │   └── __init__.py
│   ├── migrations/                  # Alembic migrasyonları
│   └── alembic.ini                  # Alembic konfigürasyonu
├── travelai/
│   ├── src/
│   │   ├── api/
│   │   │   ├── ledgers/
│   │   │   │   ├── models.py
│   │   │   │   ├── router.py
│   │   │   │   └── schemas.py
│   │   │   ├── config.py
│   │   │   └── db.py
│   │   ├── main.py
│   │   └── __init__.py
│   ├── migrations/
│   └── alembic.ini
├── requirements.txt
├── setup.py
└── README.md
```

## Notlar

- Operasyonlar için enum değerleri `monorepo/core/ledgers/config.py` dosyasında tanımlanmıştır
- Her uygulama, tüm paylaşılan (shared) operasyonları implemente etmek zorundadır