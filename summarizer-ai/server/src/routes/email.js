const express = require('express');
const { sendSummary } = require('../services/emailService');
const Summary = require('../models/Summary');

const router = express.Router();

router.post('/', async (req, res, next) => {
  try {
    const { summaryId, summaryHtml, recipients } = req.body;
    if (!recipients?.length) return res.status(400).json({ error: 'recipients required' });

    let html, plain;
    if (summaryId) {
      const s = await Summary.findById(summaryId);
      if (!s) return res.sendStatus(404);
      html = s.summaryHtml; plain = s.summaryPlain;
    } else if (summaryHtml) {
      html = summaryHtml; plain = summaryHtml.replace(/<[^>]+>/g, '');
    } else return res.status(400).json({ error: 'summaryId or summaryHtml required' });

    await sendSummary({ html, plain, to: recipients });
    res.sendStatus(202);
  } catch (e) { next(e); }
});

module.exports = router;
