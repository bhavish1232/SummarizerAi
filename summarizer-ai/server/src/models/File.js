const mongoose = require('mongoose');
const FileSchema = new mongoose.Schema({
  filename: String,
  originalName: String,
  mimeType: String,
  size: Number,
  textExtracted: String,
  createdAt: { type: Date, default: Date.now }
});
module.exports = mongoose.model('File', FileSchema);
