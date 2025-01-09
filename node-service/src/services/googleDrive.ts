import { google } from 'googleapis';
import { DaprClient} from '@dapr/dapr';
import { Credentials } from 'google-auth-library';
import { googleClientId, googleClientSecret, googleRedirectURI } from '../config/auth.config';

// Create a Dapr client with options
const daprClient = new DaprClient();

const PUBSUB_NAME = 'files'; // Dapr pub/sub component
const TOPIC_NAME = 'files';

const oauth2Client = new google.auth.OAuth2(
  googleClientId, googleClientSecret, googleRedirectURI
);

export function getAuthUrl() {
  return oauth2Client.generateAuthUrl({
    access_type: 'offline',
    scope: ['https://www.googleapis.com/auth/drive'],
  });
}

export async function handleOAuthCallback(code: string) {
  const { tokens } = await oauth2Client.getToken(code);
  oauth2Client.setCredentials(tokens);
}

const drive = google.drive({ version: 'v3', auth: oauth2Client });

// Function to list files in a specific Google Drive folder
export async function listFilesInFolder(folderId: string) {
    try {
      const response = await drive.files.list({
        q: `'${folderId}' in parents`,
        fields: 'files(id, name, mimeType, webViewLink, webContentLink)',
        pageSize: 10,
        supportsAllDrives: true,
        includeItemsFromAllDrives: true,
      });
      return response.data.files || [];
    } catch (error) {
      console.error('Error listing files:', error);
      throw error;
    }
  }

// Function to process a file in PubSub pattern
export async function downloadFile(fileId: string) {
  try {
    // Fetch file metadata
    const file = await drive.files.get({
      fileId,
      fields: 'name, mimeType',
      supportsAllDrives: true,
    });

    const fileName = file.data.name || 'unknown';
    const mimeType = file.data.mimeType || 'application/octet-stream';

    // Fetch file content
    const fileContent = await drive.files.get(
      { fileId, alt: 'media', supportsAllDrives: true },
      { responseType: 'stream' }
    );

    const chunks: Buffer[] = [];
    fileContent.data.on('data', (chunk) => chunks.push(chunk));
    fileContent.data.on('end', async () => {
      const fileBuffer = Buffer.concat(chunks);

      // Publish the file content to a Dapr pub/sub topic
      const message = {
        fileId,
        fileName,
        mimeType,
        content: fileBuffer.toString('base64'), // Save content as Base64
      };
      await daprClient.pubsub.publish(PUBSUB_NAME, TOPIC_NAME, message); 
      console.log(`File published : ${JSON.stringify(message)}`);     
    });
  } catch (error) {
    console.error('Error downloading file:', error);
    throw error;
  }
}

// Function to update file extension
export async function updateFileExtension(
  fileId: string,
  newExtension: string
) {
  try {    
    // Get the current file metadata
    const file = await drive.files.get({
      fileId: fileId,
      fields: "name",
    });

    if (!file.data.name) {
      throw new Error("File not found or missing name");
    }

    // Extract the current filename and update its extension
    const currentName = file.data.name;
    const baseName = currentName.substring(0, currentName.lastIndexOf("."));
    const newName = `${baseName}.${newExtension}`;

    // Update the file's name
    const updatedFile = await drive.files.update({
      fileId: fileId,
      requestBody: {
        name: newName,
      },
    });

    console.log(`File renamed to: ${updatedFile.data.name}`);
  } catch (error) {
    console.error("Error updating file extension:", error);
  }
}

export function isAuthenticated(): boolean {
  const credentials: Credentials = oauth2Client.credentials;
  return !!credentials.access_token && (!credentials.expiry_date || Date.now() < credentials.expiry_date);
}

export default {
    getAuthUrl, 
    handleOAuthCallback, 
    isAuthenticated,
    listFilesInFolder, 
    downloadFile,
  };
