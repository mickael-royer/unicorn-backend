import express from 'express';
import bodyParser from 'body-parser';
import googleRoutes from './routes/googleRoutes';
import { corsMiddleware } from './middleware/cors';
import { sessionMiddleware } from './middleware/session';
import { authMiddleware } from './middleware/auth';

const app = express();

app.use(corsMiddleware);
app.use(sessionMiddleware);
app.use(authMiddleware);
app.use(bodyParser.json());
app.use('/', googleRoutes);

export default app;
