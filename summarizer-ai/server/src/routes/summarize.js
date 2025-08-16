const express = require('express');
const Summary = require('../models/Summary');
const ai = require('../services/ai/openaiProvider');
const File = require('../models/File');

const router = express.Router();

router.post('/', async (req, res, next) => {
  try {
    const { prompt, text, fileId } = req.body;
    const originalText = text || (await File.findById(fileId))?.textExtracted;
    if (!prompt || !originalText) return res.status(400).json({ error: 'prompt and text/fileId required' });

    const { html, plain } = await ai.summarize({ prompt, text: originalText });
    const doc = await Summary.create({ prompt, originalText, summaryHtml: html, summaryPlain: plain });
    res.json({ summaryId: doc._id, summaryHtml: doc.summaryHtml, summaryPlain: doc.summaryPlain });
  } catch (e) { next(e); }
});

module.exports = router;
