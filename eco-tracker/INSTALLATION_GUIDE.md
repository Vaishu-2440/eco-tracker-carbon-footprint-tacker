# 🚀 EcoTracker Installation Guide

## 📋 Prerequisites

- **Python 3.8+** (Recommended: Python 3.9 or higher)
- **pip** (Python package manager)
- **Git** (optional, for cloning)

## 🔧 Installation Methods

### Method 1: Quick Start (Recommended)

1. **Navigate to project directory**
   ```bash
   cd C:\Users\mani3\Downloads\eco-tracker
   ```

2. **Run the startup script**
   ```bash
   # Windows
   start.bat
   
   # Or double-click start.bat in File Explorer
   ```

### Method 2: Manual Installation

1. **Create virtual environment**
   ```bash
   python -m venv .venv
   ```

2. **Activate virtual environment**
   ```bash
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create necessary directories**
   ```bash
   mkdir data models exports
   ```

5. **Train ML models**
   ```bash
   python src\train_model.py
   ```

6. **Run the application**
   ```bash
   streamlit run app.py
   ```

### Method 3: Using Python Runner

```bash
python run.py
```

## 🧪 Testing Installation

1. **Run test suite**
   ```bash
   python test_app.py
   ```

2. **Generate demo data**
   ```bash
   python src\demo_data.py
   ```

3. **Verify all components**
   ```bash
   python -c "from src.carbon_calculator import CarbonFootprintCalculator; print('✅ Installation successful!')"
   ```

## 🌐 Accessing the Application

1. **Open your web browser**
2. **Navigate to**: `http://localhost:8501`
3. **Create your user profile**
4. **Start tracking your carbon footprint!**

## ⚠️ Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'pandas'`
```bash
Solution: Install dependencies
pip install -r requirements.txt
```

**Issue**: `Permission denied` on database
```bash
Solution: Create data directory
mkdir data
```

**Issue**: `Port 8501 already in use`
```bash
Solution: Use different port
streamlit run app.py --server.port 8502
```

**Issue**: Model training takes too long
```bash
Solution: Use pre-trained models
python run.py --skip-training
```

### Performance Tips

- **Close other browser tabs** for better performance
- **Use Chrome or Firefox** for best compatibility
- **Ensure 4GB+ RAM** for smooth ML operations
- **Use SSD storage** for faster database operations

## 🔄 Updates and Maintenance

### Updating Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Retraining Models
```bash
python src\train_model.py
```

### Database Backup
```bash
# Backup database
copy data\eco_tracker.db data\eco_tracker_backup.db
```

### Clearing Cache
```bash
# Clear Streamlit cache
streamlit cache clear
```

## 📱 System Requirements

### Minimum Requirements
- **OS**: Windows 10, macOS 10.14, Ubuntu 18.04
- **RAM**: 2GB
- **Storage**: 500MB
- **Python**: 3.8+

### Recommended Requirements
- **OS**: Windows 11, macOS 12+, Ubuntu 20.04+
- **RAM**: 4GB+
- **Storage**: 1GB
- **Python**: 3.9+
- **Browser**: Chrome 90+, Firefox 88+

## 🎯 First Steps After Installation

1. **Create User Profile** - Enter your name and email
2. **Log First Day** - Input today's activities
3. **Explore Dashboard** - View your initial footprint
4. **Set Goals** - Create reduction targets
5. **Get Predictions** - Use AI to forecast your impact
6. **Follow Recommendations** - Implement suggested actions

## 🆘 Getting Help

If you encounter issues:

1. **Check this guide** for common solutions
2. **Review error messages** carefully
3. **Ensure all dependencies** are installed
4. **Try restarting** the application
5. **Check Python version** compatibility

---

**Happy tracking! 🌱 Let's reduce our carbon footprint together!**
