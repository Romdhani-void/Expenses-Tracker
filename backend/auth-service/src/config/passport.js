const passport = require('passport');
const LocalStrategy = require('passport-local').Strategy;
const GoogleStrategy = require('passport-google-oauth20').Strategy;
const bcrypt = require('bcrypt');
const db = require('./database');
require('dotenv').config();

// Serialize user for session
passport.serializeUser((user, done) => {
  done(null, user.id);
});

// Deserialize user from session
passport.deserializeUser(async (id, done) => {
  try {
    const result = await db.query('SELECT id, email, name FROM users WHERE id = $1', [id]);
    done(null, result.rows[0]);
  } catch (error) {
    done(error, null);
  }
});

// Local Strategy for email/password authentication
passport.use(
  new LocalStrategy(
    {
      usernameField: 'email',
      passwordField: 'password',
    },
    async (email, password, done) => {
      try {
        const result = await db.query('SELECT * FROM users WHERE email = $1', [email]);
        
        if (result.rows.length === 0) {
          return done(null, false, { message: 'Invalid email or password' });
        }

        const user = result.rows[0];
        const isValidPassword = await bcrypt.compare(password, user.password);

        if (!isValidPassword) {
          return done(null, false, { message: 'Invalid email or password' });
        }

        return done(null, user);
      } catch (error) {
        return done(error);
      }
    }
  )
);

// Google OAuth Strategy (optional - only enabled if credentials are configured)
if (process.env.GOOGLE_CLIENT_ID && process.env.GOOGLE_CLIENT_SECRET) {
  passport.use(
    new GoogleStrategy(
      {
        clientID: process.env.GOOGLE_CLIENT_ID,
        clientSecret: process.env.GOOGLE_CLIENT_SECRET,
        callbackURL: process.env.GOOGLE_CALLBACK_URL || 'http://localhost:3001/auth/google/callback',
      },
      async (accessToken, refreshToken, profile, done) => {
        try {
          // Check if user already exists
          const existingUser = await db.query(
            'SELECT * FROM users WHERE google_id = $1',
            [profile.id]
          );

          if (existingUser.rows.length > 0) {
            return done(null, existingUser.rows[0]);
          }

          // Check if email already exists
          const emailExists = await db.query(
            'SELECT * FROM users WHERE email = $1',
            [profile.emails[0].value]
          );

          if (emailExists.rows.length > 0) {
            // Link Google account to existing user
            await db.query(
              'UPDATE users SET google_id = $1 WHERE email = $2',
              [profile.id, profile.emails[0].value]
            );
            return done(null, emailExists.rows[0]);
          }

          // Create new user
          const newUser = await db.query(
            'INSERT INTO users (email, name, google_id) VALUES ($1, $2, $3) RETURNING *',
            [profile.emails[0].value, profile.displayName, profile.id]
          );

          return done(null, newUser.rows[0]);
        } catch (error) {
          return done(error);
        }
      }
    )
  );
  console.log('Google OAuth strategy enabled');
} else {
  console.warn('⚠️  Google OAuth not configured - skipping. Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET to enable.');
}

module.exports = passport;
