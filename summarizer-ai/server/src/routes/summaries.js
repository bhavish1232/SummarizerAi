const express = require('express');
const Summary = require('../models/Summary');

const router = express.Router();

router.get('/:id', async (req, res, next) => {
  try { const s = await Summary.findById(req.params.id); if (!s) return res.sendStatus(404); res.json(s); }
  catch (e) { next(e); }
});

router.get('/', async (_req, res, next) => {
  try { const list = await Summary.find().sort({ createdAt: -1 }).limit(50); res.json(list); }
  catch (e) { next(e); }
});

router.put('/:id', async (req, res, next) => {
  try {
    const { summaryHtml, summaryPlain } = req.body;
    const s = await Summary.findByIdAndUpdate(
      req.params.id,
      { summaryHtml, summaryPlain, updatedAt: new Date() },
      { new: true }
    );
    res.json(s);
  } catch (e) { next(e); }
});

module.exports = router;
