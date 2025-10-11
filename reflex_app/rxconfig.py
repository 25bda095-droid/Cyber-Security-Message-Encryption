import reflex as rx

config = rx.Config(
    app_name="fraud_detection",
    frontend_packages=[
        "recharts",
        "framer-motion",
    ],
)

# ---- APP CONFIGURATION ----
class FraudDetectionConfig(rx.Config):
    """Fraud Detection System Configuration"""
    
    # App name and branding
    app_name = "fraud_detection"
    app_title = "Fraud Detection System"
    description = "Credit Card Transaction Fraud Detection using ML Models"
    
    # Frontend configuration
    frontend_port = 3000
    frontend_host = "0.0.0.0"
    
    # Backend configuration
    backend_port = 8000
    backend_host = "0.0.0.0"
    
    # Database (optional - for storing analysis results)
    db_url = "sqlite:///fraud_detection.db"
    
    # API configuration
    api_url = "http://localhost:8000"
    
    # Tailwind CSS configuration
    tailwind = {
        "content": [
            "app/**/*.{js,ts,jsx,tsx}",
            "pages/**/*.{js,ts,jsx,tsx}",
            "components/**/*.{js,ts,jsx,tsx}",
        ],
        "theme": {
            "extend": {
                "colors": {
                    "primary": "#667eea",
                    "secondary": "#764ba2",
                    "danger": "#fc5c7d",
                    "success": "#6a82fb",
                    "warning": "#ffb800",
                    "dark": "#232946",
                },
                "fontFamily": {
                    "sans": ["Segoe UI", "Roboto", "sans-serif"],
                },
            }
        },
    }
    
    # Environment variables
    env = {
        "ENVIRONMENT": "development",
        "LOG_LEVEL": "INFO",
        "MAX_UPLOAD_SIZE": "100MB",
    }
    
    # CORS configuration for API
    cors_allowed_origins = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]
    
    # Compress assets
    compress_assets = True
    
    # Next.js configuration
    nextjs_config = {
        "reactStrictMode": True,
        "swcMinify": True,
        "images": {
            "unoptimized": True,
        },
    }
    
    # Custom headers
    headers = {
        "X-Frame-Options": "SAMEORIGIN",
        "X-Content-Type-Options": "nosniff",
        "X-XSS-Protection": "1; mode=block",
    }
    
    # Logging configuration
    logging = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
            },
        },
        "handlers": {
            "default": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
        },
        "root": {
            "level": "INFO",
            "handlers": ["default"],
        },
    }


# ---- PRODUCTION CONFIGURATION ----
class ProductionConfig(FraudDetectionConfig):
    """Production environment configuration"""
    
    env = {
        "ENVIRONMENT": "production",
        "LOG_LEVEL": "WARNING",
        "MAX_UPLOAD_SIZE": "500MB",
    }
    
    # Production CORS
    cors_allowed_origins = [
        "https://yourdomain.com",
        "https://www.yourdomain.com",
    ]
    
    # Production database
    db_url = "postgresql://user:password@localhost/fraud_detection_prod"
    
    # Compression
    compress_assets = True
    
    # Next.js production settings
    nextjs_config = {
        "reactStrictMode": False,
        "swcMinify": True,
        "productionBrowserSourceMaps": False,
        "images": {
            "unoptimized": False,
            "formats": ["image/avif", "image/webp"],
        },
    }


# ---- DEVELOPMENT CONFIGURATION ----
class DevelopmentConfig(FraudDetectionConfig):
    """Development environment configuration"""
    
    env = {
        "ENVIRONMENT": "development",
        "LOG_LEVEL": "DEBUG",
        "MAX_UPLOAD_SIZE": "100MB",
    }
    
    # Enable debugging
    nextjs_config = {
        "reactStrictMode": True,
        "swcMinify": False,
        "productionBrowserSourceMaps": True,
    }


# ---- SELECT CONFIGURATION BASED ON ENVIRONMENT ----
import os

ENVIRONMENT = os.getenv("REFLEX_ENV", "development")

if ENVIRONMENT == "production":
    config = ProductionConfig()
else:
    config = DevelopmentConfig()


# Export for Reflex
__all__ = ["config"]
