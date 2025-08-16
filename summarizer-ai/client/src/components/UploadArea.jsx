import { useState } from 'react';
import { api } from '../api/client';

export default function UploadArea({ onTextReady }) {
  const [loading, setLoading] = useState(false);
  const onChange = async (e) => {
    const file = e.target.files[0]; if (!file) return;
    const form = new FormData(); form.append('file', file);
    setLoading(true);
    try {
      const { data } = await api.post('/upload', form);
      onTextReady({ text: data.textExtracted, fileId: data.fileId });
    } catch (err) {
      alert('Upload failed: ' + (err?.response?.data?.error || err.message));
    } finally { setLoading(false); }
  };
  return (
    <div style={{margin:'12px 0'}}>
      <input type="file" accept=".txt,.pdf,.docx" onChange={onChange} />
      {loading && <small style={{marginLeft:8}}>Extracting…</small>}
    </div>
  );
}
