import { useState } from 'react';
import { api } from '../api/client';
import UploadArea from '../components/UploadArea';
import PromptBox from '../components/PromptBox';
import SummaryEditor from '../components/SummaryEditor';
import ShareModal from '../components/ShareModal';

export default function Home() {
  const [ctx, setCtx] = useState({ text: '', fileId: null });
  const [summaryId, setSummaryId] = useState(null);
  const [summaryHtml, setSummaryHtml] = useState('');
  const [showShare, setShowShare] = useState(false);
  const [loading, setLoading] = useState(false);

  const generate = async (prompt) => {
    const payload = { prompt, ...(ctx.text ? { text: ctx.text } : { fileId: ctx.fileId }) };
    setLoading(true);
    try {
      const { data } = await api.post('/summarize', payload);
      setSummaryId(data.summaryId);
      setSummaryHtml(data.summaryHtml);
    } catch (e) {
      alert('Summarize failed: ' + (e?.response?.data?.error || e.message));
    } finally { setLoading(false); }
  };

  const saveEdits = async () => {
    if (!summaryId) return;
    const plain = summaryHtml.replace(/<[^>]+>/g, '');
    try {
      await api.put(`/summaries/${summaryId}`, { summaryHtml, summaryPlain: plain });
      alert('Saved!');
    } catch (e) {
      alert('Save failed: ' + (e?.response?.data?.error || e.message));
    }
  };

  return (
    <div style={{maxWidth: 900, margin: '0 auto', padding: 24}}>
      <h1>Transcript Summarizer</h1>
      <UploadArea onTextReady={setCtx} />
      <PromptBox onGenerate={generate} />
      {loading && <p>Generating…</p>}
      {summaryHtml && (
        <>
          <SummaryEditor html={summaryHtml} setHtml={setSummaryHtml} />
          <div style={{display:'flex', gap:12, marginTop:12}}>
            <button onClick={saveEdits}>Save Edits</button>
            <button onClick={()=>setShowShare(true)}>Share via Email</button>
          </div>
        </>
      )}
      {showShare && <ShareModal summaryId={summaryId} html={summaryHtml} onClose={()=>setShowShare(false)} />}
    </div>
  );
}
