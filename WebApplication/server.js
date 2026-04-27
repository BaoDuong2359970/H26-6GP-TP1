import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';
import { CosmosClient } from "@azure/cosmos";
import { Client } from 'azure-iothub';

dotenv.config();

const app = express();

const connectionString = process.env.IOTHUB_CONNECTION_STRING;
const serviceClient = Client.fromConnectionString(connectionString);

// needed for __dirname in ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

app.post("/api/command", async (req, res) => {
  const { command, value } = req.body;

  const message = JSON.stringify({
    command: command,
    value: value
  });

  try {
    await serviceClient.open();
    await serviceClient.send("collecteur_temp", message);
    res.send("Command sent");
  } catch (err) {
    console.error(err);
    res.status(500).send("Error sending command");
  }
});

// Cosmos
const client = new CosmosClient({
  endpoint: process.env.COSMOS_ENDPOINT,
  key: process.env.COSMOS_KEY
});

const database = client.database("iotdb");
const container = database.container("container1");

// serve static files
app.use(express.static('public'));

app.get('/simulation', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'simulation.html'));
});

// API
app.get("/api/data", async (req, res) => {
  try {
    const { resources } = await container.items
      .query("SELECT * FROM c ORDER BY c.Body.date DESC")
      .fetchAll();

    res.json(resources);
  } catch (err) {
    console.error(err);
    res.status(500).send("error");
  }
});

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});