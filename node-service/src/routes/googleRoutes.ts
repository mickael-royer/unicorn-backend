import express from 'express';
import { getAuthUrl, handleOAuthCallback, isAuthenticated, listFilesInFolder, downloadFile, updateFileExtension } from '../services/googleDrive';
import { frontBaseURL, googleDriveFolder } from '../config/auth.config';

const googleRoutes = express.Router();

googleRoutes.get('/auth/google', (req, res) => {
  res.redirect(getAuthUrl());
});

googleRoutes.get('/auth/google/callback', async (req, res) => {
  const { code } = req.query;
  if (typeof code === 'string') {
    await handleOAuthCallback(code);
    res.redirect(frontBaseURL);
  } else {
    res.status(400).send('Invalid request');
  }
});

googleRoutes.get('/drive/files', async (req, res) => {
  if (!isAuthenticated()) {
    return res.status(401).json({ error: 'Not authenticated' });
  }
  const files = await listFilesInFolder(googleDriveFolder);
  res.json(files);
});

googleRoutes.post("/drive/update-file-extension", async (req, res) => {
  if (!isAuthenticated()) {
    return res.status(401).json({ error: 'Not authenticated' });
  }
  const { fileIds } = req.body;
  if (!Array.isArray(fileIds)) {
    return res.status(400).json({ error: 'Invalid input: fileIds must be an array' });
  }

  console.log('Received file IDs to update:', fileIds);

  try {
    // Iterate through fileIds and update each file
    await Promise.all(
      fileIds.map(async (fileId) => {
        const updatedName = await updateFileExtension(fileId, 'md'); 
        return {
          fileId,
          updatedName,
        };
      })
    );
    // Send response after all updates are complete
    const files = await listFilesInFolder('1ECdStkKwnMoGJt7PtzaP6838vKf1UYeJ');
    res.status(200).json(files);
  } catch (error: any) {
    console.error("Error updating file extension:", error.message);
    res.status(500).json({ error: error.message });
  }
});


// Route to download a file
googleRoutes.post('/drive/download', async (req, res) => {
  if (!isAuthenticated()) {
    return res.status(401).json({ error: 'Not authenticated' });
  }
  const { fileId } = req.body; // Extract fileId from POST body
  if (!fileId) {
    return res.status(400).json({ error: "Missing 'fileId' in request body" });
  }
  try {
    await downloadFile(fileId);
    res.status(200).send(`File ${fileId} is being processed asynchronously.`);
  } catch (error) {
    res.status(500).json({ error: 'Error downloading file' });
  }
});

export default googleRoutes;
