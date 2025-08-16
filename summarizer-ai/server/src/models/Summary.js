const mongoose = require('mongoose');
const SummarySchema = new mongoose.Schema({
  prompt: { type: String, required: true },
  originalText: { type: String, required: true },
  summaryHtml: { type: String, required: true },
  summaryPlain: { type: String, required: true },
  recipients: [String],
  createdAt: { type: Date, default: Date.now },
  updatedAt: { type: Date, default: Date.now }
});
module.exports = mongoose.model('Summary', SummarySchema);
