# LiveKit Video Conferencing App

A Next.js 15 application with LiveKit integration for real-time video conferencing, featuring comprehensive password protection for secure access.

## Features

- 🔐 **Password Protection** - Complete app-wide authentication
- 🎥 **Video Conferencing** - Real-time video chat with adaptive streaming
- 🏠 **Room Management** - Create, join, and delete video conference rooms
- 👥 **Participant Management** - Handle multiple participants with ease
- 🌐 **Vercel Ready** - Optimized for seamless deployment

## Quick Start

### 1. Clone and Install

```bash
git clone <your-repo-url>
cd vocab_ai_web_app
npm install
```

### 2. Environment Setup

Copy the example environment file and configure your settings:

```bash
cp .env.example .env.local
```

Edit `.env.local` with your configuration:

```env
# LiveKit Configuration
LIVEKIT_URL='wss://your-livekit-server.com'
LIVEKIT_API_KEY='your-api-key'
LIVEKIT_API_SECRET='your-api-secret'
NEXT_PUBLIC_LIVEKIT_URL='wss://your-livekit-server.com'

# App Password Protection
APP_PASSWORD='your-secure-password-here'
```

### 3. Run Development Server

```bash
npm run dev
```

Visit `http://localhost:3000` - you'll be prompted to enter the password before accessing the app.

## Password Protection

The app implements a robust authentication system:

### How It Works

1. **Middleware Protection**: All routes are protected by Next.js middleware
2. **Login Flow**: Unauthenticated users are redirected to `/login`
3. **Secure Authentication**: Password validation happens server-side
4. **Session Management**: Uses HTTP-only cookies for security
5. **7-Day Sessions**: Authentication persists for a week

### Security Features

- ✅ Server-side password validation
- ✅ HTTP-only cookies (XSS protection)
- ✅ Secure flag in production
- ✅ SameSite protection
- ✅ Complete app lockdown until authenticated

### Changing the Password

Update the `APP_PASSWORD` environment variable in your `.env.local` file or deployment settings.

## Deployment

### Vercel Deployment

1. Connect your GitHub repository to Vercel
2. Add environment variables in Vercel dashboard:
   - `LIVEKIT_URL`
   - `LIVEKIT_API_KEY`
   - `LIVEKIT_API_SECRET`
   - `NEXT_PUBLIC_LIVEKIT_URL`
   - `APP_PASSWORD`
3. Deploy!

### Other Platforms

The app works on any platform that supports Next.js 15. Ensure all environment variables are configured.

## Development

### Commands

```bash
npm run dev      # Start development server with Turbopack
npm run build    # Build for production
npm start        # Start production server
npm run lint     # Run ESLint
```

### Project Structure

```
├── app/
│   ├── api/
│   │   ├── auth/         # Authentication API
│   │   └── token/        # LiveKit token management
│   ├── login/            # Login page
│   ├── layout.tsx        # Root layout
│   └── page.tsx          # Main app interface
├── middleware.ts         # Password protection middleware
├── .env.example          # Environment template
└── README.md
```

## LiveKit Configuration

This app requires a LiveKit server. You can:

1. **Use LiveKit Cloud**: Sign up at [livekit.io](https://livekit.io)
2. **Self-host**: Deploy your own LiveKit server
3. **Local Development**: Run LiveKit locally for testing

## Troubleshooting

### Common Issues

**Can't access the app**
- Ensure `APP_PASSWORD` is set in your environment
- Check that the password you're entering matches exactly

**LiveKit connection issues**
- Verify all LiveKit environment variables are correct
- Ensure your LiveKit server is running and accessible
- Check browser console for WebSocket connection errors

**Build/deployment issues**
- Run `npm run build` locally to test
- Ensure all environment variables are set in production
- Check deployment logs for specific errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is private and confidential.
