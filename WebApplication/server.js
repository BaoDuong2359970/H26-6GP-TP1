import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';
import mysql from 'mysql2/promise';

dotenv.config();

const app = express();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static('public'));

const db = mysql.createPool({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME,
    waitForConnections: true
})

app.get('/simulation', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'simulation.html'));
});

app.get('/api/test-db', async (req, res) => {
    try {
        const [rows] = await db.query('SELECT 1 AS connected');
        res.json({ success: true, result: rows[0] });
    } catch (error) {
        console.error(error);
        res.status(500).json({ success: false, error: 'Database connection failed' });
    }
});

app.get('/api/latest', async (req, res) => {
    try {
        const [rows] = await db.query(`
            SELECT temperature, luminosite, ouverture, mode, status, date
            FROM data
            ORDER BY date DESC
            LIMIT 1
        `);

        if (rows.length === 0) {
            return res.json(null);
        }

        res.json(rows[0]);
    } catch(error) {
        console.error(error);
        res.status(500).json({ error: 'Error fetching last data '});
    }
});

app.get('/api/history', async (req, res) => {
    try {
        const [rows] = await db.query(`
            SELECT temperature, luminosite, ouverture, mode, status, date
            FROM data
            ORDER BY date DESC
        `);

        res.json(rows);
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Error fetching history' });
    }
});

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});