# Server Monitoring Application

A Django web application developed for monitoring and managing server status.

## Features

- **User Management** (Register, Login, Logout)
- **Server Status Monitoring**
- **Dashboard Viewing**

## Technologies

- **Python** 3.12
- **Django** 5.1.4
- **Tailwind CSS** 3.4.17
- **SQLite3**

## Installation

### Clone the project

```bash
git clone [repository-url]
cd server-monitoring
```

### Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
# venv\Scripts\activate  # For Windows
```

### Install required Python packages

```bash
pip install -r requirements.txt
```

### Install Node.js packages

```bash
npm install
```

### Apply Django migrations

```bash
python manage.py migrate
```

### Compile Tailwind CSS

```bash
npm run dev
```

### Run the application

```bash
python manage.py runserver
```

## Project Structure

```
serverMonitoring/
├── serverMonitoring/      # Main project directory
├── monitor/              # Monitor application
│   ├── templates/       # Monitor templates
│   └── static/         # Static files
├── user/                # User management application
│   ├── templates/      # User templates
│   └── views.py       # User views
├── static/             # General static files
│   ├── css/
│   └── src/
├── manage.py
├── requirements.txt
└── package.json
```

## Usage

- Create a new account at [http://127.0.0.1:8000/user/register/](http://127.0.0.1:8000/user/register/)
- Login at [http://127.0.0.1:8000/user/login/](http://127.0.0.1:8000/user/login/)
- Monitor your servers through the dashboard

## Contributing

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Create a Pull Request

## License

This project is licensed under the [LICENSE_NAME] - see the LICENSE file for details.

## Contact

[Your contact information]