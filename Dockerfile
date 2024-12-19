# Python 3.12 resmi imajını kullan
FROM python:3.12

# Node.js kurulumu için gerekli paketleri ekle
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get update && apt-get install -y nodejs

# Çalışma dizinini belirle
WORKDIR /app

# Python bağımlılıkları için requirements.txt dosyasını kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# package.json ve package-lock.json dosyalarını kopyala (eğer varsa)
COPY package*.json ./
RUN npm install

# Projenin geri kalanını kopyala
COPY . .

# Tailwind CSS'i derle
RUN npm run build

# Django statik dosyalarını topla
RUN python manage.py collectstatic --noinput

# Django için gerekli portları aç (varsayılan 8000)
EXPOSE 8000

# Başlangıç scripti oluştur
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Entrypoint script'ini kullan
ENTRYPOINT ["/app/entrypoint.sh"]