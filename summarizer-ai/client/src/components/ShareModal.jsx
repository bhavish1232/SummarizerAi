import { useState } from 'react';
import { api } from '../api/client';

export default function ShareModal({ summaryId, html, onClose }) {
  const [to, setTo] = useState('');
  const [sending, setSending] = useState(false);

  const send = async () => {
    const recipients = to.split(',').map(s=>s.trim()).filter(Boolean);
    if (!recipients.length) { alert('Enter at least one email'); return; }
    setSending(true);
    try {
      await api.post('/email', summaryId ? { summaryId, recipients } : { summaryHtml: html, recipients });
      alert('Email sent (accepted by server).');
      onClose();
    } catch (e) {
      alert('Email failed: ' + (e?.response?.data?.error || e.message));
    } finally { setSending(false); }
  };

  return (
    <div style={{border:'1px solid #999', padding:12, marginTop:12}}>
      <h3>Share via Email</h3>
      <input placeholder="alice@x.com, bob@y.com" value={to} onChange={e=>setTo(e.target.value)} style={{width:'100%'}} />
      <div style={{display:'flex', gap:8, marginTop:8}}>
        <button onClick={send} disabled={sending}>{sending ? 'Sending…' : 'Send'}</button>
        <button onClick={onClose}>Close</button>
      </div>
    </div>
  );
}
