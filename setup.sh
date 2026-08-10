#!/bin/bash

# Quick setup script for InPar Backend

echo "🚀 Starting InPar Backend Setup..."

# Navigate to project directory
cd /Users/dauren/projects/inpar

# Start Docker containers
echo "📦 Starting Docker containers..."
docker-compose up -d

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 15

# Run migrations
echo "🗄️  Running migrations..."
docker-compose exec -T backend python manage.py migrate

# Create superuser
echo "👤 Create superuser (admin)..."
docker-compose exec backend python manage.py createsuperuser

# Collect static files
echo "📁 Collecting static files..."
docker-compose exec -T backend python manage.py collectstatic --noinput

echo "✅ Setup complete!"
echo ""
echo "🌐 Access your application:"
echo "   Backend: http://localhost:8000"
echo "   Admin: http://localhost:8000/admin"
echo "   API Docs: http://localhost:8000/api"
echo ""
echo "📝 Next steps:"
echo "   1. Go to http://localhost:8000/admin"
echo "   2. Login with your superuser credentials"
echo "   3. Create categories and products"
echo "   4. Start building your frontend!"
