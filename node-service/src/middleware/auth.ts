import { auth } from 'express-openid-connect';
import { domain, clientId, secret, apiBaseURL } from '../config/auth.config';

export const authMiddleware = auth({
  authRequired: false,
  auth0Logout: true,
  issuerBaseURL: `https://${domain}`,
  baseURL: apiBaseURL,
  clientID: clientId,
  secret: secret,
  authorizationParams: {
    scope: 'openid profile email https://www.googleapis.com/auth/drive.file',
  },
});
export default authMiddleware;