const fs = require('fs');
const path = require('path');
const pdf = require('pdf-parse');
const mammoth = require('mammoth');
const textract = require('textract');

async function extractText(filePath, mime) {
  const ext = path.extname(filePath).toLowerCase();
  if (mime === 'application/pdf' || ext === '.pdf') {
    const data = await pdf(fs.readFileSync(filePath));
    return data.text;
  }
  if (ext === '.docx') {
    const result = await mammoth.extractRawText({ path: filePath });
    return result.value;
  }
  if (mime?.startsWith('text/') || ext === '.txt') {
    return fs.readFileSync(filePath, 'utf8');
  }
  // fallback
  return new Promise((resolve, reject) => {
    textract.fromFileWithPath(filePath, (err, text) => err ? reject(err) : resolve(text));
  });
}
module.exports = { extractText };
