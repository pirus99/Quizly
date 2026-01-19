# Quizly - AI-Powered Quiz Generator from YouTube Videos

Quizly is a Django REST API application that automatically generates interactive quizzes from YouTube videos. It uses OpenAI Whisper for audio transcription and OpenAI-compatible LLMs for intelligent quiz generation.

## Features

- 🎥 **YouTube Video Processing**: Download and extract audio from YouTube videos
- 🎙️ **Speech-to-Text**: Transcribe video audio using OpenAI Whisper
- 🤖 **AI Quiz Generation**: Create comprehensive quizzes using OpenAI-compatible LLMs
- 👤 **User Authentication**: JWT-based authentication system with secure cookie management
- 📝 **Quiz Management**: Create, read, update, and delete quizzes
- 🔒 **Secure**: CORS protection, CSRF tokens, and proper authentication

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher**
- **pip** (Python package manager)
- **FFmpeg** (required for audio processing)

### Installing FFmpeg

FFmpeg is essential for audio extraction from YouTube videos. Choose your operating system:

#### Windows
```bash
# Using Chocolatey
choco install ffmpeg

# Using Scoop
scoop install ffmpeg

# Or download manually from: https://ffmpeg.org/download.html
# Add FFmpeg to your system PATH
```

#### macOS
```bash
# Using Homebrew
brew install ffmpeg
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install ffmpeg
```

#### Linux (Fedora)
```bash
sudo dnf install ffmpeg
```

Verify FFmpeg installation:
```bash
ffmpeg -version
```

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/pirus99/Quizly.git
   cd Quizly
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # Activate on Windows
   venv\Scripts\activate
   
   # Activate on macOS/Linux
   source venv/bin/activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and configure the following variables:
   
   ```env
   # OpenAI API Configuration
   OPENAI_ENDPOINT=https://openrouter.ai/api/v1
   OPENAI_API_KEY=your_api_key_here
   OPENAI_MODEL=meta-llama/llama-3.3-70b-instruct:free
   
   # Whisper Model Configuration
   # Options: tiny(1GB), base(1GB), small(2GB), medium(5GB), large(10GB), turbo(6GB)
   WHISPER_MODEL=tiny
   
   # Django Configuration
   DJANGO_SECRET_KEY=your_secret_key_here
   DJANGO_DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   
   # Server Configuration
   PORT=8000
   ```
   
   **Important Notes:**
   - Generate a secure `DJANGO_SECRET_KEY` using: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
   - Set `DJANGO_DEBUG=False` in production
   - Choose appropriate Whisper model based on your hardware (GPU recommended for larger models)
   - Get your OpenAI API key from [OpenRouter](https://openrouter.ai/) or your preferred OpenAI-compatible provider

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser** (optional, for admin access)
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**
   ```bash
   python manage.py runserver
   ```
   
   Or specify a custom port:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

The API will be available at `http://localhost:8000/`

## API Endpoints

### Authentication

- **POST** `/api/auth/register/` - Register a new user
- **POST** `/api/auth/login/` - Login and receive JWT tokens
- **POST** `/api/auth/refresh/` - Refresh access token
- **POST** `/api/auth/logout/` - Logout and invalidate tokens

### Quiz Management

- **POST** `/api/quiz/create/` - Create a quiz from a YouTube URL
  ```json
  {
    "url": "https://www.youtube.com/watch?v=VIDEO_ID"
  }
  ```

- **GET** `/api/quiz/list/` - List all quizzes for authenticated user
- **GET** `/api/quiz/<quiz_id>/` - Get a specific quiz
- **PATCH** `/api/quiz/<quiz_id>/` - Update a quiz
- **DELETE** `/api/quiz/<quiz_id>/` - Delete a quiz

## Project Structure

```
Quizly/
├── core/                   # Django project settings
│   ├── settings.py        # Main configuration file
│   ├── urls.py            # Root URL configuration
│   └── wsgi.py            # WSGI configuration
├── quiz_app/              # Quiz application
│   ├── api/
│   │   ├── views.py       # Quiz API endpoints
│   │   ├── services.py    # Core business logic
│   │   ├── serializers.py # Data serialization
│   │   └── prompt.py      # AI prompts
│   └── models.py          # Database models
├── jwt_auth_app/          # Authentication application
│   ├── api/
│   │   ├── views.py       # Auth API endpoints
│   │   └── authentication.py # Custom JWT auth
│   └── models.py          # User models
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
└── .env.example           # Example environment variables
```

## Usage Example

1. **Register a user:**
   ```bash
   curl -X POST http://localhost:8000/api/auth/register/ \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "email": "test@example.com", "password": "securepass123"}'
   ```

2. **Login:**
   ```bash
   curl -X POST http://localhost:8000/api/auth/login/ \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "password": "securepass123"}' \
     -c cookies.txt
   ```

3. **Create a quiz from YouTube video:**
   ```bash
   curl -X POST http://localhost:8000/api/quiz/create/ \
     -H "Content-Type: application/json" \
     -b cookies.txt \
     -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
   ```

## Development

### Running Tests
```bash
python manage.py test
```

### Code Style
This project follows PEP 8 style guidelines. Key conventions:
- Use docstrings for complex functions
- Keep code readable and well-commented
- Follow Django best practices

## Troubleshooting

### FFmpeg Not Found
**Error:** `ffmpeg not found in PATH`

**Solution:** Ensure FFmpeg is installed and added to your system PATH. Restart your terminal after installation.

### CUDA/GPU Issues
If you encounter GPU-related errors with Whisper:
- The application will automatically fall back to CPU
- For better performance with larger models, ensure CUDA is properly installed
- Consider using a smaller Whisper model (e.g., `tiny` or `base`) on CPU

### API Rate Limits
If you're using a free OpenAI-compatible API:
- Be aware of rate limits
- Consider upgrading to a paid plan for production use
- Implement retry logic if needed

### Database Errors
If you encounter database issues:
```bash
# Delete the database and start fresh
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

## Environment Variables Reference

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_ENDPOINT` | OpenAI-compatible API endpoint | - | Yes |
| `OPENAI_API_KEY` | API key for OpenAI service | - | Yes |
| `OPENAI_MODEL` | Model name for quiz generation | - | Yes |
| `WHISPER_MODEL` | Whisper model size | `small` | No |
| `DJANGO_SECRET_KEY` | Django secret key | - | Yes |
| `DJANGO_DEBUG` | Enable debug mode | `True` | No |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `localhost,127.0.0.1` | No |
| `PORT` | Server port | `8000` | No |

## Security Considerations

- Never commit `.env` file to version control
- Use strong `DJANGO_SECRET_KEY` in production
- Set `DJANGO_DEBUG=False` in production
- Configure proper `ALLOWED_HOSTS` for your domain
- Use HTTPS in production
- Regularly update dependencies for security patches

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) - Speech recognition
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube video downloading
- [Django](https://www.djangoproject.com/) - Web framework
- [Django REST Framework](https://www.django-rest-framework.org/) - REST API toolkit

## Support

For issues, questions, or contributions, please open an issue on GitHub.
