#!/bin/bash

echo "🌿 AyurAI Setup Script"
echo "======================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ and try again."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ and try again."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install Python dependencies"
    exit 1
fi

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
npm install

if [ $? -ne 0 ]; then
    echo "❌ Failed to install Node.js dependencies"
    exit 1
fi

echo "✅ Setup completed successfully!"
echo ""
echo "🚀 To start the application:"
echo "1. Start the backend: python app.py"
echo "2. Start the frontend: npm start"
echo ""
echo "🌐 The application will be available at http://localhost:3000"
echo "📡 The API will be available at http://localhost:5000"