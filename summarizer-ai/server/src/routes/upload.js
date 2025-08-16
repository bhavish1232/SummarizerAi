const express = require('express');
const multer = require('multer');
const path = require('path');
const File = require('../models/File');
const { extractText } = require('../services/parseService');

const router = express.Router();
const upload = multer({ dest: path.join(__dirname, '../../uploads') });

router.post('/', upload.single('file'), async (req, res, next) => {
  try {
    const textExtracted = await extractText(req.file.path, req.file.mimetype);
    const file = await File.create({
      filename: req.file.filename,
      originalName: req.file.originalname,
      mimeType: req.file.mimetype,
      size: req.file.size,
      textExtracted
    });
    res.json({ fileId: file._id, textExtracted });
  } catch (e) { next(e); }
});

module.exports = router;
