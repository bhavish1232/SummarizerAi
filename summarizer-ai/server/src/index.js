require('dotenv').config();
const express = require('express');
require('./config/mongo');
const cors = require("cors");

app.use(cors({
  origin: "*",   // abhi ke liye sab allowed
}));

const uploadRoutes = require('./routes/upload');
const summarizeRoutes = require('./routes/summarize');
const emailRoutes = require('./routes/email');
const summariesRoutes = require('./routes/summaries');
const error = require('./middleware/error');

const app = express();

app.use(express.json({ limit: '5mb' }));

app.get('/api/health', (_req, res) => res.json({ ok: true }));

app.use('/api/upload', uploadRoutes);
app.use('/api/summarize', summarizeRoutes);
app.use('/api/email', emailRoutes);
app.use('/api/summaries', summariesRoutes);

app.use(error);

const PORT = process.env.PORT || 4000;
app.listen(PORT, () => console.log(`API running on ${PORT}`));
