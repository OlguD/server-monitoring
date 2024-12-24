# build.sh dosyası oluştur
echo '#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate' > build.sh

# Çalıştırma izni ver
chmod +x build.sh