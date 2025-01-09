import session from 'express-session';

const uuid = require('uuid');
const sessionSecret = process.env.SESSION_SECRET || uuid.v4();

export const sessionMiddleware = session({
  secret: sessionSecret,
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: false,
    httpOnly: true,
    maxAge: 24 * 60 * 60 * 1000,
  },
});
export default sessionMiddleware;