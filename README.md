# InternshipHub - Verified Internship Platform

A comprehensive web platform connecting students with verified internship opportunities from trusted companies and government organizations. Built with Flask and modern web technologies.

## 🌟 Features

### For Students
- **Profile Management**: Create detailed profiles with education, skills, and document verification
- **Aadhar Verification**: Secure verification through DigiLocker integration
- **Smart Search**: Advanced filtering by company type, category, location, and skills
- **Application Tracking**: Monitor application status and manage submissions
- **Mobile Responsive**: Fully optimized for mobile devices

### For Companies
- **Verified Listings**: All internships are from verified trust companies and government organizations
- **Detailed Information**: Comprehensive internship details including requirements, duration, and stipend
- **Category Organization**: Organized by technology, business, research, healthcare, and education
- **Real-time Updates**: Fresh opportunities updated regularly

### Platform Features
- **Modern UI/UX**: Clean, intuitive interface with smooth animations
- **Security**: Secure user authentication and data protection
- **Performance**: Fast loading and responsive design
- **Accessibility**: Mobile-friendly and accessible design

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or Download** the project files to your local machine

2. **Run the startup script** (Windows):
   ```bash
   start_server.bat
   ```
   
   Or manually:
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Run the application
   python app.py
   ```

3. **Open your browser** and navigate to `http://localhost:5000`

## 📱 Mobile Support

The platform is fully responsive and optimized for mobile devices:
- Touch-friendly interface
- Mobile navigation menu
- Optimized forms and layouts
- Fast loading on mobile networks

## 🏢 Company Types

### Trust Companies
- Verified non-profit organizations
- Educational institutions
- Research foundations
- Social impact organizations

### Government Organizations
- Ministry internships
- Public sector undertakings
- Government research institutes
- Policy and administration roles

### Private Companies
- Technology startups
- Corporate internships
- Industry partnerships
- Innovation labs

## 📊 Categories

- **Technology**: Software development, AI/ML, cybersecurity, UI/UX
- **Business**: Marketing, finance, operations, strategy
- **Research**: Scientific research, innovation, development
- **Healthcare**: Medical research, healthcare technology
- **Education**: Educational technology, teaching, curriculum development

## 🔧 Technical Details

### Backend
- **Framework**: Flask (Python)
- **Database**: SQLite (easily upgradeable to PostgreSQL/MySQL)
- **Authentication**: Session-based with secure password hashing
- **API**: RESTful API endpoints for data access

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with Flexbox and Grid
- **JavaScript**: Vanilla JS for interactivity
- **Icons**: Font Awesome
- **Fonts**: Inter (Google Fonts)

### Features
- **Responsive Design**: Mobile-first approach
- **Form Validation**: Client and server-side validation
- **Error Handling**: User-friendly error messages
- **Security**: CSRF protection, input sanitization

## 📁 Project Structure

```
InternshipHub/
├── app.py                 # Flask backend application
├── requirements.txt       # Python dependencies
├── start_server.bat      # Windows startup script
├── test_system.py        # System testing script
├── README.md             # This file
├── static/
│   ├── styles.css        # Main stylesheet
│   └── script.js         # JavaScript functionality
├── templates/
│   ├── index.html        # Homepage
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── dashboard.html    # User dashboard
│   ├── internships.html  # Browse internships
│   ├── internship_detail.html # Individual internship page
│   └── profile.html      # User profile page
└── data/
    └── internships.json  # Sample internship data
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
python test_system.py
```

The test suite checks:
- Server connectivity
- Page loading
- API endpoints
- User registration
- Mobile responsiveness
- CSS/JS loading

## 🔐 Security Features

- **Password Hashing**: Secure password storage using Werkzeug
- **Session Management**: Secure session handling
- **Input Validation**: Server-side validation for all inputs
- **CSRF Protection**: Cross-site request forgery protection
- **SQL Injection Prevention**: Parameterized queries

## 📈 Future Enhancements

- **Email Notifications**: Application status updates
- **Advanced Search**: AI-powered matching
- **Company Dashboard**: For organizations to manage listings
- **Resume Builder**: Integrated resume creation
- **Video Interviews**: Built-in interview scheduling
- **Analytics Dashboard**: Application tracking and insights

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Email: support@internshiphub.com
- Phone: +91 98765 43210
- Address: 123 Innovation Street, Tech City, India

## 🙏 Acknowledgments

- Flask community for the excellent framework
- Font Awesome for the beautiful icons
- Google Fonts for the Inter typeface
- All the open-source contributors who made this possible

---

**InternshipHub** - Connecting students with verified internship opportunities from trusted companies and government organizations.

© 2024 InternshipHub. All rights reserved.
