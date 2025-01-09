require('dotenv').config();
import app from './app';
import { DaprServer } from "@dapr/dapr";

const daprHost = process.env.DAPR_HOST || 'localhost';
const daprPort = process.env.DAPR_PORT || '3500';
const serverHost = process.env.SERVER_HOST || 'localhost';
const serverPort = process.env.SERVER_PORT || '3001';

/** 
app.listen(serverPort, () => {
  console.log(`Server running at http://${serverHost}:${serverPort}`);
});

**/

const daprServer = new DaprServer({
  serverHost,
  serverPort,
  serverHttp: app,
  clientOptions: {
    daprHost,
    daprPort,
  },
});

daprServer.start().then(() => {
  console.log(`Server running at http://${serverHost}:${serverPort}`);
});
/** */