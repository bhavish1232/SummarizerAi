const transporter = require('../config/mailer');

async function sendSummary({ html, plain, to }) {
  const info = await transporter.sendMail({
    from: process.env.MAIL_FROM || process.env.SMTP_USER,
    to: to.join(','),
    subject: "Shared Summary",
    text: plain,
    html
  });
  return info.messageId;
}
module.exports = { sendSummary };
