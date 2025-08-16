const { pipeline } = require('@xenova/transformers');

let summarizer;

async function loadSummarizer() {
  if (!summarizer) {
    // Chhota aur fast model
    summarizer = await pipeline('summarization', 'Xenova/t5-small');
  }
  return summarizer;
}

module.exports.summarize = async ({ prompt, text }) => {
  const model = await loadSummarizer();
  const output = await model(text, { max_length: 200, min_length: 30, do_sample: false });

  const plain = output[0].summary_text;
  const html = `<p>${plain}</p>`;

  return { plain, html };
};
