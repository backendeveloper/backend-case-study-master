#!/usr/bin/env bash

# Hata ayıklama için
set -e

# Sanal ortam oluştur ve bağımlılıkları yükle
if [ ! -d "venv" ]; then
    echo "Sanal ortam oluşturuluyor..."
    python -m venv venv
fi

# Sanal ortamı aktif et
source venv/bin/activate

# Bağımlılıkları yükle
echo "Bağımlılıklar yükleniyor..."
pip install -e .

# PostgreSQL veritabanlarını oluştur
echo "Veritabanları oluşturuluyor..."
createdb -U postgres healthai || echo "healthai veritabanı zaten var"
createdb -U postgres travelai || echo "travelai veritabanı zaten var"

# HealthAI için migrasyonları çalıştır
echo "HealthAI migrasyonları çalıştırılıyor..."
cd healthai
alembic upgrade head
cd ..

# TravelAI için migrasyonları çalıştır
# echo "TravelAI migrasyonları çalıştırılıyor..."
# cd travelai
# alembic upgrade head
# cd ..

# HealthAI uygulamasını başlat
echo "HealthAI uygulaması başlatılıyor..."
cd healthai
uvicorn src.main:app --reload --port 8000 &
cd ..

# TravelAI uygulamasını başlat
# echo "TravelAI uygulaması başlatılıyor..."
# cd travelai
# uvicorn src.main:app --reload --port 8001 &
# cd ..

echo "Uygulama çalışıyor:"
echo "HealthAI: http://localhost:8000"
echo "TravelAI: http://localhost:8001"
echo "Durdurmak için Ctrl+C tuşlarına basın..."

# Her iki uygulamanın da çalışmasını bekle
wait